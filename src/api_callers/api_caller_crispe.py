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
        "cost_per_1M_input": 1.50,
        "cost_per_1M_output": 6.00
    }
}

FOCC_JSON_PATH = Path("artifacts/programs/focc/all_programs_foccs.json")
COVERAGE_JSON_PATH = Path("artifacts/programs/runner_programs_with_coverage.json")
BASE_OUTPUT_DIR = Path("API_Model_Outputs_CRISPE_no_examplar")

DRY_RUN = False
NUM_OUTPUTS_PER_PROMPT = 5
MAX_PROGRAMS_TO_PROCESS = None
MAX_WORKERS = 20
DELAY_BETWEEN_CALLS = 0.1

INCLUDE_DATASETS = ["CRUXEval", "HumanEval", "PythonSaga"]


def load_crispe_prompt_template():
    """Load CRISPE prompt template"""
    crispe_path = Path("data/prompts/reasoning/crispe_predict_coverage_original.txt")
    if crispe_path.exists():
        template = crispe_path.read_text(encoding="utf-8")
        print(f"Loaded CRISPE template: {crispe_path}")
        return template
    else:
        print(f"Missing CRISPE template: {crispe_path}")
        exit














def setup_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment")
    return openai.OpenAI(api_key=api_key)

def initialize_clients():
    print("Initializing API clients...")
    for model_name, config in MODELS_CONFIG.items():
        try:
            if config["provider"] == "openai":
                config["client"] = setup_openai_client()
            print(f"{model_name} client initialized")
        except Exception as e:
            print(f"Failed to initialize {model_name}: {e}")
            config["client"] = None


def load_combined_data():
    """Load data strictly from JSONs"""


    if FOCC_JSON_PATH.exists():
        with open(FOCC_JSON_PATH, 'r', encoding='utf-8') as f:
            focc_data = json.load(f)
        print(f"Loaded {len(focc_data)} programs from FOCC file")
    else:
        print(f"Warning: FOCC file not found at {FOCC_JSON_PATH}")
        focc_data = []


    if not COVERAGE_JSON_PATH.exists():
        print(f"ERROR: Coverage data file '{COVERAGE_JSON_PATH}' not found.")
        exit(1)

    with open(COVERAGE_JSON_PATH, 'r', encoding='utf-8') as f:
        coverage_data = json.load(f)
    print(f"Loaded {len(coverage_data)} programs from coverage file")


    focc_lookup = {}
    for item in focc_data:
        program_id = item.get("program_id", "")
        if program_id:

            focc_lookup[program_id] = item

            if '/' in program_id:
                underscore_id = program_id.replace('/', '_')
                focc_lookup[underscore_id] = item


    combined_data = []

    for program in coverage_data:
        dataset = program.get("dataset", "")
        if dataset not in INCLUDE_DATASETS:
            continue

        task_id = program.get("task_id", "")
        if not task_id:
            continue


        original_code = program.get("runnable_script", "")
        if not original_code:
            continue


        focc_item = None
        if task_id in focc_lookup:
            focc_item = focc_lookup[task_id]
        else:

            underscore_id = task_id.replace('/', '_')
            if underscore_id in focc_lookup:
                focc_item = focc_lookup[underscore_id]


        foccs = []
        test_case = ""
        if focc_item:
            foccs = focc_item.get("foccs", [])
            test_case = focc_item.get("test_case", "")


        dir_id = task_id.replace('/', '_')

        combined_data.append({
            "program_id": dir_id,
            "original_task_id": task_id,
            "dataset": dataset,
            "original_code": original_code,
            "test_case": test_case,
            "foccs": foccs,
            "coverage_metadata": program.get("coverage_metadata", {})
        })

    print(f"Combined {len(combined_data)} programs for processing")
    return combined_data

def filter_programs_by_dataset(programs, included_datasets):
    """Filter programs by dataset"""
    if not included_datasets:
        return programs

    filtered = [p for p in programs if p.get("dataset") in included_datasets]


    counts = {}
    for p in filtered:
        ds = p.get("dataset", "Unknown")
        counts[ds] = counts.get(ds, 0) + 1

    print("Dataset Breakdown:")
    for ds, count in counts.items():
        print(f"  - {ds}: {count}")

    return filtered


def add_line_numbers(code):
    """Add line numbers to code without stripping"""
    lines = code.split('\n')
    return "\n".join(f"Line {i}: {line}" for i, line in enumerate(lines, 1))

def build_crispe_prompt(crispe_template, program_data):
    original_code = program_data.get("original_code", "")
    if not original_code:
        return None


    numbered_code = add_line_numbers(original_code)


    test_case = program_data.get("test_case", "")
    if not test_case:

        lines = original_code.split('\n')
        for line in reversed(lines):
            if 'assertEqual' in line or 'assertTrue' in line or 'assertFalse' in line:

                import re
                match = re.search(r'assert(?:Equal|True|False)\(([^,]+)', line)
                if match:
                    test_case = match.group(1).strip()
                    break

    complete_program = numbered_code
    if test_case:
        complete_program += f"\n\nGIVEN TEST CASE:\n{test_case}"


    foccs = program_data.get("foccs", [])
    if foccs and len(foccs) > 0:
        focc_text = "GIVEN POSSIBLE SETS OF CODE COVERAGE:\n"
        for i, focc in enumerate(foccs, 1):
            line_str = ", ".join(map(str, focc))
            focc_text += f"{i}. Lines [{line_str}]\n"
    else:
        focc_text = "No pre-computed execution paths available."

    return crispe_template.replace("{program_code}", complete_program).replace("{FOCC}", focc_text.strip())


def call_model_api(model_name, prompt_text, max_retries=3):
    """Unified API call function with retry logic"""
    model_config = MODELS_CONFIG[model_name]

    if DRY_RUN:
        response_text = f"--- DRY RUN RESPONSE ({model_name}) ---\n\nPredicted coverage: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
        estimated_tokens = len(prompt_text) // 4
        usage_info = {
            "input_tokens": estimated_tokens,
            "output_tokens": 100,
            "total_tokens": estimated_tokens + 100
        }
        return response_text, usage_info

    for attempt in range(max_retries):
        try:
            client = model_config["client"]
            response = client.chat.completions.create(
                model=model_config["model"],
                messages=[{"role": "user", "content": prompt_text}],

                max_completion_tokens=8192
            )
            response_text = response.choices[0].message.content
            usage_info = {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
            return response_text, usage_info
        except openai.RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Rate limit hit, retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            else:
                print(f"Rate limit error after {max_retries} retries")
                return f"Rate limit error", {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
        except Exception as e:
            print(f"API Error for {model_name} (attempt {attempt+1}): {e}")
            if attempt == max_retries - 1:
                return f"Error: {e}", {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
            time.sleep(1)

    return "Max retries exceeded", {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}


def process_single_api_call(args):
    """Worker function for ThreadPoolExecutor"""
    model_name, prompt_text, output_dir = args

    response_text, usage_info = call_model_api(model_name, prompt_text)


    (output_dir / "crispe_coverage_response.txt").write_text(response_text)


    input_cost = (usage_info["input_tokens"] / 1_000_000) * MODELS_CONFIG[model_name]["cost_per_1M_input"]
    output_cost = (usage_info["output_tokens"] / 1_000_000) * MODELS_CONFIG[model_name]["cost_per_1M_output"]
    total_cost = input_cost + output_cost

    (output_dir / "crispe_coverage_usage.json").write_text(json.dumps({
        "usage_info": usage_info,
        "cost_breakdown": {
            "input_tokens": usage_info["input_tokens"],
            "output_tokens": usage_info["output_tokens"],
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": total_cost
        }
    }, indent=2))

    return {
        "model_name": model_name,
        "usage_info": usage_info,
        "cost": total_cost
    }

def prepare_program_tasks(program_data, crispe_template):
    program_id = program_data["program_id"]
    dataset = program_data["dataset"]

    prompt_text = build_crispe_prompt(crispe_template, program_data)
    if not prompt_text:
        print(f"Skipping {program_id} - could not build prompt")
        return []

    foccs = program_data.get("foccs", [])
    model_name = "gpt-5-mini"

    model_dir = BASE_OUTPUT_DIR / model_name
    model_dir.mkdir(exist_ok=True, parents=True)

    tasks = []
    for output_num in range(1, NUM_OUTPUTS_PER_PROMPT + 1):
        output_dir = model_dir / program_id / f"output_{output_num}"
        output_dir.mkdir(exist_ok=True, parents=True)

        (output_dir / "crispe_coverage_prompt.txt").write_text(prompt_text)
        (output_dir / "program_metadata.json").write_text(json.dumps({
            "program_id": program_id,
            "original_task_id": program_data.get("original_task_id", ""),
            "dataset": dataset,
            "has_foccs": len(foccs) > 0,
            "focc_count": len(foccs),
            "call_number": output_num,
            "timestamp": time.time()
        }, indent=2))

        tasks.append((model_name, prompt_text, output_dir))
    return tasks


def main():
    start_time = time.time()

    print("=" * 80)
    print("CRISPE API Experiment Runner - gpt-5-mini")
    print("=" * 80)
    print(f"Target model: gpt-5-mini")
    print(f"Datasets: {INCLUDE_DATASETS}")
    print(f"Outputs per program: {NUM_OUTPUTS_PER_PROMPT}")
    print(f"Dry run: {DRY_RUN}")
    print(f"Parallel workers: {MAX_WORKERS}")
    print("=" * 80)


    initialize_clients()


    if not DRY_RUN and MODELS_CONFIG["gpt-5-mini"]["client"] is None:
        print("OpenAI client not initialized. Check OPENAI_API_KEY environment variable.")
        exit(1)


    combined_data = load_combined_data()
    combined_data = filter_programs_by_dataset(combined_data, INCLUDE_DATASETS)

    if MAX_PROGRAMS_TO_PROCESS:
        combined_data = combined_data[:MAX_PROGRAMS_TO_PROCESS]
        print(f"Limiting to {len(combined_data)} programs for testing")


    crispe_template = load_crispe_prompt_template()


    BASE_OUTPUT_DIR.mkdir(exist_ok=True)


    print("\nPhase 1: Preparing tasks...")
    all_api_tasks = []

    for program_data in tqdm(combined_data, desc="Preparing programs"):
        tasks = prepare_program_tasks(program_data, crispe_template)
        all_api_tasks.extend(tasks)

    print(f"Prepared {len(all_api_tasks)} API tasks from {len(combined_data)} programs")


    if not DRY_RUN:

        avg_input_tokens = 2000
        avg_output_tokens = 200
        input_cost_per_call = (avg_input_tokens / 1_000_000) * MODELS_CONFIG["gpt-5-mini"]["cost_per_1M_input"]
        output_cost_per_call = (avg_output_tokens / 1_000_000) * MODELS_CONFIG["gpt-5-mini"]["cost_per_1M_output"]
        total_cost_per_call = input_cost_per_call + output_cost_per_call
        estimated_total_cost = total_cost_per_call * len(all_api_tasks)

        print(f"\nEstimated cost for {len(all_api_tasks)} API calls:")
        print(f"   Per call: ${total_cost_per_call:.6f}")
        print(f"   Total: ${estimated_total_cost:.2f}")


        print("\n" + "="*60)
        print("LIVE MODE - Real API calls will be made")
        print("="*60)
        confirm = input(f"Proceed with {len(all_api_tasks)} API calls? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Aborting script.")
            exit(0)
    else:
        print("\nDry run: DRY RUN MODE - No real API calls will be made")
        print("   Prompt files will be created but no API calls")


    print(f"\nStarting Phase 2: Executing API calls...")
    experiment_stats = {
        "total_calls": len(all_api_tasks),
        "completed": 0,
        "failed": 0,
        "total_input_tokens": 0,
        "total_output_tokens": 0,
        "total_cost": 0.0
    }


    BATCH_SIZE = min(50, len(all_api_tasks))

    for batch_start in range(0, len(all_api_tasks), BATCH_SIZE):
        batch_end = min(batch_start + BATCH_SIZE, len(all_api_tasks))
        batch = all_api_tasks[batch_start:batch_end]

        print(f"\nProcessing batch {batch_start//BATCH_SIZE + 1}/{(len(all_api_tasks) + BATCH_SIZE - 1)//BATCH_SIZE}")
        print(f"   Calls {batch_start + 1} to {batch_end} of {len(all_api_tasks)}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(process_single_api_call, args) for args in batch]

            with tqdm(total=len(batch), desc="Batch progress") as pbar:
                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                        experiment_stats["completed"] += 1

                        if not DRY_RUN:
                            experiment_stats["total_input_tokens"] += result["usage_info"]["input_tokens"]
                            experiment_stats["total_output_tokens"] += result["usage_info"]["output_tokens"]
                            experiment_stats["total_cost"] += result["cost"]

                        pbar.update(1)
                        pbar.set_postfix({
                            "Cost": f"${experiment_stats['total_cost']:.2f}" if not DRY_RUN else "DRY_RUN",
                            "Completed": experiment_stats["completed"]
                        })


                        if not DRY_RUN:
                            time.sleep(DELAY_BETWEEN_CALLS)

                    except Exception as e:
                        print(f"Error in API call: {e}")
                        experiment_stats["failed"] += 1
                        pbar.update(1)


    stats_file = BASE_OUTPUT_DIR / "experiment_stats.json"
    stats_file.write_text(json.dumps({
        "model": "gpt-5-mini",
        "experiment": "CRISPE Coverage Prediction",
        "timestamp": time.time(),
        "duration_seconds": time.time() - start_time,
        "programs_processed": len(combined_data),
        "api_calls": len(all_api_tasks),
        "stats": experiment_stats,
        "configuration": {
            "num_outputs_per_prompt": NUM_OUTPUTS_PER_PROMPT,
            "max_workers": MAX_WORKERS,
            "include_datasets": INCLUDE_DATASETS,
            "dry_run": DRY_RUN,
            "delay_between_calls": DELAY_BETWEEN_CALLS
        }
    }, indent=2))


    duration = time.time() - start_time
    print("\n" + "="*80)
    print("EXPERIMENT COMPLETED")
    print("="*80)
    print(f"Duration: {duration:.2f}s ({duration/60:.2f}m)")
    print(f"Results directory: {BASE_OUTPUT_DIR}")
    print(f"Programs processed: {len(combined_data)}")
    print(f"API calls: {experiment_stats['completed']} completed, {experiment_stats['failed']} failed")

    if not DRY_RUN:
        print(f"   Total cost: ${experiment_stats['total_cost']:.4f}")
        print(f"   Input tokens: {experiment_stats['total_input_tokens']:,}")
        print(f"   Output tokens: {experiment_stats['total_output_tokens']:,}")
        print(f"   Cost per program: ${experiment_stats['total_cost']/len(combined_data):.4f}")
    else:
        print("  Mode: DRY RUN - No actual costs incurred")

    print("="*80)

if __name__ == "__main__":
    main()