import json
from statistics import mean
from grading import grade_syntax_all, grade_by_model

with open("eval/tasks.json", "r") as f:
    dataset = json.load(f)

with open("eval/outputs_v2.json", "r") as f:
    outputs = json.load(f)

all_model_grades = grade_by_model(dataset, outputs)
all_syntax_scores = grade_syntax_all(outputs, dataset)

final_result = []

for i in range(len(dataset)):
    model_grade = all_model_grades[i]
    syntax_score = all_syntax_scores[i]
    final_score = (model_grade["score"] + syntax_score) / 2

    final_result.append(
        {
            "task": dataset[i]['task'],
            "format": dataset[i]["format"],
            "output": outputs[i]["output"],
            "model_score": model_grade["score"],
            "syntax_score": syntax_score,
            "final_score": final_score,
            "reasoning": model_grade["reasoning"],
        }
    )

with open("eval/final_eval_v2.json", "w") as f:
    json.dump(final_result, f, indent=2)

print("Eval complete. Results are saved to final_eval_v2.json")
