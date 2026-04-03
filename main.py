from utils.parser import load_data
from core.model import GridModel
from core.validator import check_supply_demand
from core.validator import check_connectivity
from core.validator import check_line_capacity
from core.validator import check_isolated_nodes
from core.validator import check_redundancy
from core.validator import check_bottlenecks
from core.suggestion import generate_suggestions
from utils.formatter import format_output

def main():
    print("Running GridGuard...")

    data = load_data("input.json")
    model = GridModel(data)

    errors = []
    warnings = []

    # Supply
    result = check_supply_demand(model)
    if "ERROR" in result:
        errors.append(result)

    # Connectivity
    for err in check_connectivity(model):
        errors.append(err)

    # Capacity
    for err in check_line_capacity(model):
        errors.append(err)

    # Isolation + redundancy → warnings
    for warn in check_isolated_nodes(model):
        warnings.append(warn)

    for warn in check_redundancy(model):
        warnings.append(warn)

    # Suggestions
    suggestions = generate_suggestions(model)

    # FINAL OUTPUT
    format_output(errors, warnings, suggestions)

if __name__ == "__main__":
    main()