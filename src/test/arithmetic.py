from ..executor import CobralangExecutor
import colorama
import json
import os

if __name__ == '__main__':
    executor = CobralangExecutor()
    tests = [
        {
            "cobra": "6 + 19 + 6 - 39 + 1359 - 19",
            "python": "6 + 19 + 6 - 39 + 1359 - 19",
        },
        {
            "cobra": "1 + 6 - 1 / 58 - 1 + 26 % 159 / 6359 % 19 + (18 * 8)",
            "python": "1 + 6 - 1 / 58 - 1 + 26 % 159 / 6359 % 19 + (18 * 8)"
        },
        {
            "cobra": "1 + 58 - (1 / 6 - 1) + 26 % 159 / (6359 // 19) + ((18 * 8) + 7) ** 2 + (6 * 12)",
            "python": "1 + 58 - (1 / 6 - 1) + 26 % 159 / (6359 // 19) + ((18 * 8) + 7) ** 2 + (6 * 12)"
        },
        {
            "cobra": "--------------5",
            "python": "--------------5"
        },
        {
            "cobra": "8 + 8 > 28 - 1 * 8 % 2 // 6 * 1",
            "python": "8 + 8 > 28 - 1 * 8 % 2 // 6 * 1"
        },
        {
            "cobra": "true and true == (false != (not false)) or true",
            "python": "True and True == (False != (not False)) or True"
        }
    ]
    failed_tests = []

    for test_num, test in enumerate(tests):
        python_result = eval(test["python"])
        if isinstance(python_result, bool):
            python_result = "true" if python_result else "false"
        else:
            python_result = str(float(python_result))

        cobra_result = str(executor.execute("<test>", [test["cobra"]], {}).value).lower()
        if python_result == cobra_result:
            print(f"Test {test_num + 1} passed.")
        else:
            print(f"{colorama.Fore.RED}Test {test_num + 1} failed!{colorama.Style.RESET_ALL}")
            failed_tests.append({
                "test_num": test_num + 1,
                "python": test["python"],
                "cobra": test["cobra"],
                "python_result": python_result,
                "cobra_result": cobra_result
            })

    print(f"{len(tests)} tests completed. {len(tests) - len(failed_tests)} tests passed, "
          f"{len(failed_tests)} tests failed. {(len(tests) - len(failed_tests)) / len(tests) * 100}% success rate.")

    with open(os.path.join(os.path.dirname(__file__), "failed.json"), "w+") as f:
        json.dump(failed_tests, f, indent=4)
