import papermill as pm

next_version = input("Enter New version!\n")


pm.execute_notebook(
    "feedback_loop.ipynb",
    f"./output/notebooks/feedback-loop_output_{next_version}.ipynb",
    parameters={"SEARCH_VERSION": next_version},
)
