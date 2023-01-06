from aio_proxy.response.helpers import is_dev_env


def format_response(
    formatted_search_results, total_results, page, per_page, execution_time
):
    response = {
        "results": formatted_search_results,
        "total_results": int(total_results),
        "page": page + 1,
        "per_page": per_page,
    }
    remainder_results = response["total_results"] % response["per_page"]
    response["total_pages"] = (
        response["total_results"] // response["per_page"]
        if remainder_results == 0
        else response["total_results"] // response["per_page"] + 1
    )
    # Include execution time in response if current env is dev
    if is_dev_env():
        response["execution_time"] = execution_time
    return response
