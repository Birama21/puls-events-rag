import json
from pathlib import Path

from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualRelevancyMetric,
)
from deepeval.test_case import LLMTestCase
from deepeval.models.base_model import DeepEvalBaseLLM

from langchain_mistralai import ChatMistralAI

from src.rag import ask, retrieve_context


DATASET_PATH = Path("evaluation/test_dataset.json")


class MistralEvaluator(DeepEvalBaseLLM):
    """LLM Mistral utilisé comme juge par DeepEval."""

    def __init__(self):
        self.model = ChatMistralAI(
            model="mistral-small-latest",
            temperature=0,
        )

    def load_model(self):
        return self.model

    def generate(self, prompt: str, schema=None):
        response = self.model.invoke(prompt)
        return response.content

    async def a_generate(self, prompt: str, schema=None):
        response = await self.model.ainvoke(prompt)
        return response.content

    def get_model_name(self):
        return "Mistral Small"


def load_dataset():
    """Charge le jeu de test annoté."""

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def main():

    dataset = load_dataset()

    print("=" * 70)
    print("ÉVALUATION RAG - DEEPEVAL")
    print("=" * 70)
    print(f"{len(dataset)} questions\n")

    evaluator = MistralEvaluator()

    metrics = [
        AnswerRelevancyMetric(
            threshold=0.5,
            model=evaluator,
            include_reason=False,
        ),
        FaithfulnessMetric(
            threshold=0.5,
            model=evaluator,
            include_reason=False,
        ),
        ContextualRelevancyMetric(
            threshold=0.5,
            model=evaluator,
            include_reason=False,
        ),
    ]

    metric_names = [
        "Answer Relevancy",
        "Faithfulness",
        "Contextual Relevancy",
    ]

    scores = {
        "Answer Relevancy": [],
        "Faithfulness": [],
        "Contextual Relevancy": [],
    }

    for i, item in enumerate(dataset, start=1):

        question = item["question"]

        print(f"[{i}/{len(dataset)}] {question}")

        try:
            # Réponse générée par le RAG
            answer = ask(question)

            # VRAIS documents récupérés par FAISS
            context = retrieve_context(question)

            test_case = LLMTestCase(
                input=question,
                actual_output=answer,
                expected_output=item.get("expected_answer"),
                retrieval_context=context,
            )

            for metric, metric_name in zip(metrics, metric_names):

                try:
                    metric.measure(test_case)

                    score = metric.score

                    if score is not None:
                        scores[metric_name].append(score)

                        print(
                            f"    {metric_name:<25}: {score:.3f}"
                        )
                    else:
                        print(
                            f"    {metric_name:<25}: N/A"
                        )

                except Exception as error:

                    print(
                        f"    {metric_name:<25}: ERREUR"
                    )
                    print(
                        f"      {type(error).__name__}: {error}"
                    )

        except Exception as error:

            print("    ERREUR pendant le test")
            print(
                f"      {type(error).__name__}: {error}"
            )

        print()

    print("=" * 70)
    print("SCORES MOYENS")
    print("=" * 70)

    for metric_name, values in scores.items():

        if values:
            average = sum(values) / len(values)
            print(f"{metric_name:<25}: {average:.3f}")
        else:
            print(f"{metric_name:<25}: N/A")

    print("=" * 70)
    print("ÉVALUATION TERMINÉE")
    print("=" * 70)


if __name__ == "__main__":
    main()