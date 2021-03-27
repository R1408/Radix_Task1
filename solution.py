import csv
from datetime import datetime, timedelta

# name of csv file
filename = "input.csv"

output_rows = []
total_elements = []
reversal_overlayed_elements = []
element_data = {}


def main():
    """
    Read data from input.csv file and calculate the final value, then generate result.csv file.
    """
    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')

        for row in reader:
            if row[1] != "date":
                row[1] = row[1].replace("--", "-")
                current_dt = datetime.strptime(row[1], '%d-%m-%Y')
                element_details = {'date': current_dt, 'element': row[0], 'value': row[2],
                                   'overlayed': row[3]}
                if row[3] == "Y":
                    row.append('150')
                else:
                    reversal_overlayed_elements.append(element_details)
                total_elements.append(element_details)
                output_rows.append(row)

    reversal_elements = list(map(calculate_smallest_overlayed_element, reversal_overlayed_elements))
    for row in output_rows:
        if row[3] == "N":
            if not reversal_elements[0][row[2]]:
                row.append(row[2])
            else:
                row.append(reversal_elements[0][row[2]]['value'])

    write_output_in_result_file()


def calculate_smallest_overlayed_element(el):
    """
    Calculate the smallest overlayed element data from current date to before 12 months.
    :param el: reversal overlayed element (element whose overlayed value is 'N')
    """
    element_list = []
    global element_data

    for i in total_elements:
        if el['date'] - timedelta(days=365) <= i['date'] < el['date'] and el['element'] == i['element'] and i[
            'overlayed'] == "Y":
            element_list.append(i)
    sorted_list = sorted(element_list, key=lambda i: i['date'])
    smallest_overlayed_element = sorted_list[0] if sorted_list else sorted_list
    element_data[el["value"]] = smallest_overlayed_element
    return element_data


def write_output_in_result_file():
    """
    Generate the result.csv file and write the values.
    :return:
    """
    filename = "result.csv"
    fields = ['element', 'date', 'value', 'value_overlayed', 'final_value']
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, escapechar='-', quoting=csv.QUOTE_NONE)
        csvwriter.writerow(fields)
        csvwriter.writerows(output_rows)


if __name__ == "__main__":
    main()