import json
from statistics import mean
from gradings import grade_by_model

with open("dataset.json", "r") as f:
    dataset = json.load(f)

with open("v1/outputs_v1.json", "r") as f:
    outputs = json.load(f)

all_model_grades = grade_by_model(dataset, outputs)

final_result = []

for i in range(len(dataset)):
    final_score = all_model_grades[i]["score"]

    final_result.append(
        {
            "athlete_info": dataset[i],
            "output": outputs[i]["output"],
            "final_score": final_score,
            "reasoning": all_model_grades[i]["reasoning"],
        }
    )

with open("v1/final_eval_v1.json", "w") as f:
    json.dump(final_result, f, indent=2)

print("Eval complete. Results are saved to final_eval_v1.json")
