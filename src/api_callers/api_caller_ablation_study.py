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
    "gpt-5-mini": {
        "provider": "openai",
        "model": "gpt-5-mini",
        "type": "reasoning",
        "client": None,
        "cost_per_1M_input": 0.25,
        "cost_per_1M_output": 2.00
    }
}

COVERAGE_JSON_PATH = Path("artifacts/programs/ablation_study_programs_with_coverage.json")
BASE_OUTPUT_DIR = Path("API_Model_Outputs_Ablation")

DRY_RUN = False
NUM_OUTPUTS_PER_PROMPT = 5
MAX_PROGRAMS_TO_PROCESS = None
DELAY_BETWEEN_CALLS = 0.05
MAX_WORKERS = 20

INCLUDE_DATASETS = ["CRUXEval", "HumanEval", "PythonSaga"]

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


def setup_openai_client():
    """Setup OpenAI client"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment")
    return openai.OpenAI(api_key=api_key)

def initialize_clients():
    """Initialize API clients"""
    print("Initializing API clients...")

    for model_name, config in MODELS_CONFIG.items():
        try:
            if config["provider"] == "openai":
                config["client"] = setup_openai_client()
            print(f"{model_name} client initialized")
        except Exception as e:
            print(f"Failed to initialize {model_name}: {e}")
            config["client"] = None


def call_openai_api_batch(model_config, prompt_text):
    """Optimized OpenAI API call with graceful fallbacks"""
    try:
        client = model_config["client"]
        base_params = {
            "model": model_config["model"],
            "messages": [{"role": "user", "content": prompt_text}],
            "max_completion_tokens": 2048
        }

        try:
            response = client.chat.completions.create(
                **base_params,
                temperature=0.7,
                top_p=0.9
            )
        except Exception as e1:
            msg = str(e1).lower()

            if "top_p" in msg and "unsupported" in msg:
                try:
                    response = client.chat.completions.create(
                        **base_params,
                        temperature=0.7
                    )
                except Exception as e2:
                    msg2 = str(e2).lower()
                    if "temperature" in msg2 and "unsupported" in msg2:
                        response = client.chat.completions.create(**base_params)
                    else:
                        raise
            elif "temperature" in msg and "unsupported" in msg:
                try:
                    response = client.chat.completions.create(
                        **base_params,
                        top_p=0.9
                    )
                except Exception as e3:
                    msg3 = str(e3).lower()
                    if "top_p" in msg3 and "unsupported" in msg3:
                        response = client.chat.completions.create(**base_params)
                    else:
                        raise
            else:
                raise

        response_text = response.choices[0].message.content
        usage_info = {
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens
        }
        return response_text, usage_info

    except Exception as e:
        error_msg = f"OpenAI API Error: {str(e)}"
        print(f"{error_msg}")
        return error_msg, {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}

def call_model_api(model_name, prompt_text):
    """Unified API call function"""
    model_config = MODELS_CONFIG[model_name]

    if DRY_RUN:
        response_text = f"--- DRY RUN ({model_name}) ---\nPrompt length: {len(prompt_text)} chars"
        usage_info = {"input_tokens": len(prompt_text)//4, "output_tokens": 100, "total_tokens": len(prompt_text)//4 + 100}
        return response_text, usage_info

    if model_config["provider"] == "openai":
        return call_openai_api_batch(model_config, prompt_text)
    else:
        error_msg = f"Unknown provider: {model_config['provider']}"
        return error_msg, {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}


def add_line_numbers(code):
    """Add line numbers to code"""
    return "\n".join(f"{i:3d} | {line}" for i, line in enumerate(code.splitlines(), 1))

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

        model_name = "gpt-5-mini"
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

                pbar.update(1)
                pbar.set_postfix({
                    "Cost": f"${experiment_stats['total_costs']['estimated_cost']:.2f}" if not DRY_RUN else "DRY_RUN",
                    "Completed": experiment_stats["completed_calls"]
                })

            except Exception as e:
                error_msg = f"Error in API call: {str(e)}"
                print(error_msg)
                if not DRY_RUN:
                    experiment_stats["failed_calls"] += 1
                pbar.update(1)



def validate_program_data(programs):
    """Validate that programs have unique content and correct structure"""
    print("\nValidating program data...")

    code_samples = {}
    duplicates = 0

    for i, program in enumerate(programs[:10]):
        task_id = program["task_id"]
        code = program["runnable_script"]
        priority_line = program["coverage_metadata"]["advanced_priority_line"]


        print(f"  {task_id}:")
        print(f"    Priority line: {priority_line}")
        print(f"    Code snippet: {code[:100]}...")


        if code in code_samples:
            duplicates += 1
            print(f"    DUPLICATE of {code_samples[code]}")
        else:
            code_samples[code] = task_id

    if duplicates > 0:
        print(f"Found {duplicates} duplicate programs in first 10 samples")
    else:
        print("All sampled programs have unique content")

def debug_prompt_generation(template, programs_sample):
    """Debug prompt generation to see what's being inserted"""
    print("\nDebugging prompt generation...")

    for i, program in enumerate(programs_sample[:3]):
        task_id = program["task_id"]
        code = program["runnable_script"]
        priority_line = program["coverage_metadata"]["advanced_priority_line"]

        print(f"\n--- Prompt for {task_id} ---")
        print(f"Priority line: {priority_line}")
        print(f"Code length: {len(code)} chars")
        print(f"First 200 chars of code: {code[:200]}...")


        formatted_prompt = format_ablation_prompt(template, code, priority_line)
        print(f"Generated prompt length: {len(formatted_prompt)} chars")
        print(f"First 300 chars of prompt: {formatted_prompt[:300]}...")
        print("---")


def format_ablation_prompt(template, program_code, priority_line):
    """Replace placeholders with code and priority line for ablation study"""
    print(f"Formatting prompt - Code: {len(program_code)} chars, Priority: {priority_line}")

    numbered = add_line_numbers(program_code)
    formatted = template.replace("{program_code}", numbered)
    formatted = formatted.replace("{priority_line}", str(priority_line))


    if "{program_code}" in formatted:
        print("PROGRAM CODE NOT REPLACED!")
    if "{priority_line}" in formatted:
        print("PRIORITY LINE NOT REPLACED!")

    return formatted



def main():
    start_time = time.time()

    print(" ABLATION STUDY: Input Generation Experiment ")
    print(f"Model: gpt-5-mini")
    print(f"Coverage data: {COVERAGE_JSON_PATH}")
    print(f"Outputs per program: {NUM_OUTPUTS_PER_PROMPT}")
    print(f"Parallel workers: {MAX_WORKERS}")


    initialize_clients()


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

    validate_program_data(coverage_data)


    coverage_data = filter_programs_by_dataset(coverage_data, INCLUDE_DATASETS)


    template = load_ablation_template()
    if not template:
        print("No ablation template loaded. Exiting.")
        exit(1)


    debug_prompt_generation(template, coverage_data)



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
        print("DRY RUN MODE - No real API calls")


        if coverage_data:
            sample_program = coverage_data[0]
            task_id = sample_program["task_id"]
            code = sample_program["runnable_script"]
            priority_line = sample_program["coverage_metadata"]["advanced_priority_line"]
            sample_prompt = format_ablation_prompt(template, code, priority_line)

            print(f"\n Sample ablation prompt ({task_id}):")
            print("=" * 50)
            print(sample_prompt[:500] + "..." if len(sample_prompt) > 500 else sample_prompt)
            print("=" * 50)
    else:
        print("LIVE MODE - Real API calls will be made")
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


    BATCH_SIZE = min(50, total_programs)

    with tqdm(total=total_api_calls, desc="API Calls") as pbar:
        for i in range(0, total_programs, BATCH_SIZE):
            batch = coverage_data[i:i + BATCH_SIZE]
            process_program_batch(batch, template, experiment_stats, pbar)
            print(f"Completed batch {i//BATCH_SIZE + 1}/{(total_programs + BATCH_SIZE - 1)//BATCH_SIZE}")


    stats_file = BASE_OUTPUT_DIR / "ablation_experiment_stats.json"
    stats_file.write_text(json.dumps(experiment_stats, indent=2))


    duration = time.time() - start_time
    print(f"\nABLATION STUDY COMPLETED")
    print(f"Duration: {duration:.2f}s ({duration/60:.2f}m)")
    print(f"Results: {BASE_OUTPUT_DIR}")

    if not DRY_RUN:
        print(f"Total Cost: ${experiment_stats['total_costs']['estimated_cost']:.2f}")
        print(f"API Calls: {experiment_stats['completed_calls']} completed, {experiment_stats['failed_calls']} failed")

if __name__ == "__main__":
    main()