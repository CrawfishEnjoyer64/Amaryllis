#Welcome to normalizeData, where all data either comes in normal, or is made normal
#Presently, the file has every line has this format, delimited by asterisks (*)

#2026-11-04
#{'ADMINISTRATION': '27.0', 'DEFENCE': '0.0', 'EDUCATION': '18.5', 'ENVIRONMENT': '10.6', 'HEALTHCARE': '10.6', 'COMMERCE': '6.3', 'INTERNATIONALAID': '4.6', 'LAWANDORDER': '6.5', 'PUBLICTRANSPORT': '0.7', 'SOCIALEQUALITY': '8.5', 'SPIRITUALITY': '4.1', 'WELFARE': '2.4'}
#{'Old Age': '44.9', 'Lost in Wilderness': '14.7', 'Suicide While in Police Custody': '0.4', 'Bungee Jumping': '5.3', 'Acts of God': '16.1', 'Disappearance': '16.9', 'Accident': '1.7'}
#72.8

#This serves to translate it to the following format:

#Date, ADMINISTRATION, DEFENCE ... [n categories of spending], Old Age, Lost in Wilderness, .... [n categories of death], Public_Spending

### followed by...

###2026-11-04, ADMINISTRATION%, DEFENCE%, ... [n percentages of spending], Old Age, Lost in Wilderness, .... [n percentages of death], Public_Spending%

#Out of curiousity
num_of_entries = 0

dynamic_spending_list = []
dynamic_deaths_list = []

with open("output_data.txt") as unnormalized_data_file:
    for line in unnormalized_data_file:
        line_items = line.split('*')
        if(len(line_items) == 4): #Delimiting being performed normally indictates that the line as anticipated.
            
            item_spending_dictionary = eval(line_items[1]) #Evil
            item_death_dictionary = eval(line_items[2]) #Evil

            for spending_area in item_spending_dictionary.keys():
                if not (spending_area in dynamic_spending_list):
                    dynamic_spending_list.append(spending_area)


            for death_cause in item_death_dictionary.keys():
                if not (death_cause in dynamic_deaths_list):
                    dynamic_deaths_list.append(death_cause)
        
        num_of_entries += 1

dynamic_spending_list.sort()
dynamic_deaths_list.sort()

lines_to_write_to_file = []

first_line = "Date"
for spending_area in dynamic_spending_list:
    first_line += (",spend%_" + spending_area)
for death_cause in dynamic_deaths_list:
    first_line += (",cause%_" + death_cause)
first_line += ",public_spend%"

lines_to_write_to_file.append(first_line)

#This is a mechanism for assigning particular slots to particular spending areas and causes of death.
#...As their position in their respective arrays of all possible areas and causes.
#The following goes back through out the whole file to get each row written out.

with open("output_data.txt") as unnormalized_data_file:
    for line in unnormalized_data_file:
        
        line_desc_text = ""

        line_spending_dictionary = {}
        line_deaths_dictionary = {}

        line_items = line.split('*')
        if(len(line_items) == 4): #Delimiting being performed normally indictates that the line is how we anticipate.
            line_desc_text += line_items[0]
            
            line_spending_dictionary = eval(line_items[1]) #Evil
            line_deaths_dictionary = eval(line_items[2]) #Evil

            #For every area or cause *not* in the dictionaries already, add an entry with it set to 0.
            #This can be undesirable later, but is simple enough to correct in spreadsheet software.
            for spending_area in dynamic_spending_list:
                if(not (spending_area in line_spending_dictionary.keys())):
                    line_spending_dictionary[spending_area] = 0
            for cause in dynamic_deaths_list:
                if(not (cause in line_deaths_dictionary.keys())):
                    line_deaths_dictionary[cause] = 0

            #Output as CSV using dynamic spending list (which is alphabetized so it 
            #should always get the same order given the same present fields)
            for spending_area in dynamic_spending_list:
                line_desc_text += ("," + str(line_spending_dictionary[spending_area]))

            for cause in dynamic_deaths_list:
                line_desc_text += ("," + str(line_deaths_dictionary[cause]))

            item_public_percentage = line_items[3]
            line_desc_text += ("," + item_public_percentage)
        else:
            line_desc_text = line[:10]

        lines_to_write_to_file.append(line_desc_text.strip())

with open("normalized_data.txt", "a") as f:
    for row in lines_to_write_to_file:
        f.write((row + "\n"))

print(str(num_of_entries) + " entries processed. Thank you for your time.")