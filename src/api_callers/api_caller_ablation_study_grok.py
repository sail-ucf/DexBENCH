import os
import time
import json
import concurrent.futures
from pathlib import Path
from tqdm import tqdm
from dotenv import load_dotenv
import openai


load_dotenv()


MODELS_CONFIG = {
    "grok-4-fast-reasoning": {
        "provider": "xai",
        "model": "grok-4-fast-reasoning",
        "type": "reasoning",
        "client": None,
        "cost_per_1M_input": 2.00,
        "cost_per_1M_output": 10.00
    }
}


COVERAGE_JSON_PATH = Path("artifacts/programs/ablation_study_programs_with_coverage.json")
BASE_OUTPUT_DIR = Path("API_Model_Outputs_Ablation_grok")


DRY_RUN = False
NUM_OUTPUTS_PER_PROMPT = 5
MAX_PROGRAMS_TO_PROCESS = None
DELAY_BETWEEN_CALLS = 0.1
MAX_WORKERS = 10


INCLUDE_DATASETS = ["CRUXEval", "HumanEval", "PythonSaga"]


def setup_xai_client():
    """Setup xAI client for grok"""
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        raise ValueError("XAI_API_KEY not found in environment")
    return openai.OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1"
    )

def initialize_clients():
    """Initialize API clients"""
    print("Initializing API clients...")

    for model_name, config in MODELS_CONFIG.items():
        try:
            if config["provider"] == "xai":
                config["client"] = setup_xai_client()
            print(f"{model_name} client initialized")
        except Exception as e:
            print(f"Failed to initialize {model_name}: {e}")
            config["client"] = None


def call_xai_api_batch(model_config, prompt_text):
    """Call xAI API with proper error handling"""
    try:
        client = model_config["client"]

        response = client.chat.completions.create(
            model=model_config["model"],
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.7,
            max_tokens=2048
        )

        response_text = response.choices[0].message.content
        usage_info = {
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
        return response_text, usage_info

    except Exception as e:
        error_msg = f"xAI API Error: {str(e)}"
        print(f"{error_msg}")
        return error_msg, {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}

def call_model_api(model_name, prompt_text):
    """Unified API call function - FIXED for DRY_RUN"""
    model_config = MODELS_CONFIG[model_name]

    if DRY_RUN:
        response_text = f"--- DRY RUN ({model_name}) ---\nPrompt length: {len(prompt_text)} chars\n"
        response_text += f"Prompt preview: {prompt_text[:200]}...\n"
        response_text += f"[ANSWER]\n{{\"predicted_input\": \"test_input_for_dry_run\"}}\n[/ANSWER]"
        usage_info = {"input_tokens": len(prompt_text)//4, "output_tokens": 100, "total_tokens": len(prompt_text)//4 + 100}
        return response_text, usage_info

    if model_config["provider"] == "xai":
        return call_xai_api_batch(model_config, prompt_text)
    else:
        error_msg = f"Unknown provider: {model_config['provider']}"
        return error_msg, {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}


def load_ablation_template():
    """Load ablation study prompt template"""
    reasoning_dir = Path("data/prompts/reasoning")
    template_path = reasoning_dir / "ablation_ask_predict_input.txt"

    if template_path.exists():
        template = template_path.read_text(encoding="utf-8")
        print(f"Loaded ablation template: {template_path}")
        return template
    else:
        print(f"Missing ablation template: {template_path}")
        return None


def add_line_numbers(code):
    """Add line numbers to code"""
    lines = code.splitlines()
    return "\n".join(f"{i:3d} | {line}" for i, line in enumerate(lines, 1))

def format_ablation_prompt(template, program_code, priority_line):
    """Replace placeholders with code and priority line for ablation study"""
    numbered = add_line_numbers(program_code)
    formatted = template.replace("{program_code}", numbered)
    formatted = formatted.replace("{priority_line}", str(priority_line))
    return formatted


def filter_programs_by_dataset(coverage_data, included_datasets):
    """Filter programs based on included datasets"""
    if not included_datasets:
        return coverage_data

    filtered_programs = []
    for program in coverage_data:
        dataset = program.get("dataset", "Unknown")
        if dataset in included_datasets:
            filtered_programs.append(program)

    print(f"Filtered to {len(filtered_programs)} programs from {included_datasets}")
    return filtered_programs


def process_single_api_call(args):
    """Process a single API call - optimized for parallel execution"""
    model_name, prompt_text, output_dir, call_id = args


    response_text, usage_info = call_model_api(model_name, prompt_text)


    (output_dir / f"ablation_input_response.txt").write_text(response_text)
    (output_dir / f"ablation_input_usage.json").write_text(json.dumps({
        "usage_info": usage_info,
        "cost_breakdown": {
            "input_tokens": usage_info["input_tokens"],
            "output_tokens": usage_info["output_tokens"],
            "input_cost": (usage_info["input_tokens"] / 1_000_000) * MODELS_CONFIG[model_name]["cost_per_1M_input"],
            "output_cost": (usage_info["output_tokens"] / 1_000_000) * MODELS_CONFIG[model_name]["cost_per_1M_output"],
            "total_cost": (usage_info["input_tokens"] / 1_000_000) * MODELS_CONFIG[model_name]["cost_per_1M_input"] +
                         (usage_info["output_tokens"] / 1_000_000) * MODELS_CONFIG[model_name]["cost_per_1M_output"]
        }
    }, indent=2))

    return {
        "model_name": model_name,
        "call_id": call_id,
        "response_text": response_text,
        "usage_info": usage_info
    }

def process_program_batch(programs_batch, template, experiment_stats, pbar):
    """Process a batch of programs in parallel"""
    api_call_args = []

    for program in programs_batch:
        task_id = program["task_id"]
        dir_name = task_id.replace("/", "_")
        code = program["runnable_script"]


        priority_line = program["coverage_metadata"]["advanced_priority_line"]

        model_name = "grok-4-fast-reasoning"
        program_dir = BASE_OUTPUT_DIR / model_name / dir_name
        program_dir.mkdir(exist_ok=True, parents=True)


        formatted_prompt = format_ablation_prompt(template, code, priority_line)


        for output_num in range(1, NUM_OUTPUTS_PER_PROMPT + 1):
            output_dir = program_dir / f"output_{output_num}"
            output_dir.mkdir(exist_ok=True, parents=True)


            prompt_file = output_dir / "ablation_input_prompt.txt"
            prompt_file.write_text(formatted_prompt)


            api_call_args.append((model_name, formatted_prompt, output_dir, output_num))

    print(f"Processing batch of {len(programs_batch)} programs -> {len(api_call_args)} API calls")


    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_single_api_call, args) for args in api_call_args]

        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()


                if not DRY_RUN:
                    experiment_stats["completed_calls"] += 1
                    experiment_stats["total_costs"]["input_tokens"] += result["usage_info"]["input_tokens"]
                    experiment_stats["total_costs"]["output_tokens"] += result["usage_info"]["output_tokens"]
                    experiment_stats["total_costs"]["total_tokens"] += result["usage_info"]["total_tokens"]


                    input_cost = (result["usage_info"]["input_tokens"] / 1_000_000) * MODELS_CONFIG[result["model_name"]]["cost_per_1M_input"]
                    output_cost = (result["usage_info"]["output_tokens"] / 1_000_000) * MODELS_CONFIG[result["model_name"]]["cost_per_1M_output"]
                    total_cost = input_cost + output_cost

                    experiment_stats["total_costs"]["estimated_cost"] += total_cost
                else:

                    experiment_stats["completed_calls"] += 1

                pbar.update(1)
                pbar.set_postfix({
                    "Cost": f"${experiment_stats['total_costs']['estimated_cost']:.2f}" if not DRY_RUN else "DRY_RUN",
                    "Completed": experiment_stats["completed_calls"]
                })


                if not DRY_RUN:
                    time.sleep(DELAY_BETWEEN_CALLS)

            except Exception as e:
                error_msg = f"Error in API call: {str(e)}"
                print(error_msg)
                experiment_stats["failed_calls"] += 1
                pbar.update(1)


def main():
    start_time = time.time()

    print("=== ABLATION STUDY (GROK-4-FAST-REASONING): Input Generation Experiment ===")
    print(f"Model: grok-4-fast-reasoning")
    print(f"Coverage data: {COVERAGE_JSON_PATH}")
    print(f"Outputs per program: {NUM_OUTPUTS_PER_PROMPT}")
    print(f"Parallel workers: {MAX_WORKERS}")
    print(f"Delay between calls: {DELAY_BETWEEN_CALLS}s")
    print(f"DRY_RUN mode: {DRY_RUN}")


    initialize_clients()


    if not DRY_RUN and MODELS_CONFIG["grok-4-fast-reasoning"]["client"] is None:
        print("xAI client not initialized. Check XAI_API_KEY environment variable.")
        exit(1)


    if not COVERAGE_JSON_PATH.exists():
        print(f"ERROR: Ablation study coverage file '{COVERAGE_JSON_PATH}' not found.")
        exit(1)

    try:
        with open(COVERAGE_JSON_PATH, "r", encoding="utf-8") as f:
            coverage_data = json.load(f)
        print(f"Loaded {len(coverage_data)} programs from ablation study data")
    except Exception as e:
        print(f"ERROR: Could not parse JSON: {e}")
        exit(1)


    coverage_data = filter_programs_by_dataset(coverage_data, INCLUDE_DATASETS)


    if MAX_PROGRAMS_TO_PROCESS:
        coverage_data = coverage_data[:MAX_PROGRAMS_TO_PROCESS]
        print(f"Limiting to {len(coverage_data)} programs for testing")


    template = load_ablation_template()
    if not template:
        print("No ablation template loaded. Exiting.")
        exit(1)


    BASE_OUTPUT_DIR.mkdir(exist_ok=True)


    total_programs = len(coverage_data)
    total_api_calls = total_programs * NUM_OUTPUTS_PER_PROMPT

    print(f"\nExperiment Scale:")
    print(f"  Programs: {total_programs}")
    print(f"  Outputs per program: {NUM_OUTPUTS_PER_PROMPT}")
    print(f"  Total API calls: {total_api_calls}")

    if DRY_RUN:
        print("\n" + "="*60)
        print("DRY RUN MODE - No real API calls will be made")
        print("="*60)


        if coverage_data:
            sample_program = coverage_data[0]
            task_id = sample_program["task_id"]
            code = sample_program["runnable_script"]
            priority_line = sample_program["coverage_metadata"]["advanced_priority_line"]
            sample_prompt = format_ablation_prompt(template, code, priority_line)

            print(f"\nSample ablation prompt ({task_id}):")
            print("=" * 50)
            print(sample_prompt[:500] + "..." if len(sample_prompt) > 500 else sample_prompt)
            print("=" * 50)
    else:
        print("\n" + "="*60)
        print("LIVE MODE - Real API calls will be made")
        print("="*60)
        confirm = input("Proceed? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Aborting script.")
            exit(0)


    experiment_stats = {
        "total_programs": total_programs,
        "total_api_calls": total_api_calls,
        "completed_calls": 0,
        "failed_calls": 0,
        "total_costs": {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "estimated_cost": 0.0
        }
    }


    BATCH_SIZE = min(10, total_programs) if DRY_RUN else min(20, total_programs)

    with tqdm(total=total_api_calls, desc="API Calls") as pbar:
        for i in range(0, total_programs, BATCH_SIZE):
            batch = coverage_data[i:i + BATCH_SIZE]
            print(f"\nProcessing batch {i//BATCH_SIZE + 1}/{(total_programs + BATCH_SIZE - 1)//BATCH_SIZE}")
            process_program_batch(batch, template, experiment_stats, pbar)
            print(f"Completed batch {i//BATCH_SIZE + 1}")


    stats_file = BASE_OUTPUT_DIR / "ablation_experiment_stats_grok.json"
    stats_file.write_text(json.dumps(experiment_stats, indent=2))


    duration = time.time() - start_time
    print(f"\n ABLATION STUDY (GROK) COMPLETED")
    print(f"Duration: {duration:.2f}s ({duration/60:.2f}m)")
    print(f"Results: {BASE_OUTPUT_DIR}")

    if not DRY_RUN:
        print(f"Total Cost: ${experiment_stats['total_costs']['estimated_cost']:.2f}")
        print(f"API Calls: {experiment_stats['completed_calls']} completed, {experiment_stats['failed_calls']} failed")
        print(f"Estimated cost breakdown:")
        print(f"- Input tokens: {experiment_stats['total_costs']['input_tokens']:,} (${experiment_stats['total_costs']['input_tokens']/1_000_000 * MODELS_CONFIG['grok-4-fast-reasoning']['cost_per_1M_input']:.2f})")
        print(f"- Output tokens: {experiment_stats['total_costs']['output_tokens']:,} (${experiment_stats['total_costs']['output_tokens']/1_000_000 * MODELS_CONFIG['grok-4-fast-reasoning']['cost_per_1M_output']:.2f})")
    else:
        print(f"Dry Run Summary:")
        print(f"   - Total calls simulated: {experiment_stats['completed_calls']}")
        print(f"   - Failed calls: {experiment_stats['failed_calls']}")

if __name__ == "__main__":
    main()