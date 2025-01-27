from pymongo import MongoClient
from datetime import datetime, timedelta


client = MongoClient(
    'not sharing')
db = client['WaterManagement']


client.drop_database('WaterManagement')
print("The WaterManagement database has been dropped and will be recreated.")




def create_lookup_table(collection_name, data):
    collection = db[collection_name]
    for entry in data:
        collection.insert_one({"Description": entry})



optimization_types = ["Energy Efficiency", "Leak Detection", "Water Recycling"]
contract_statuses = ["Active", "Pending", "Cancelled"]
customer_relevances = ["High", "Medium", "Low"]
program_types = ["Residential", "Industrial", "Business"]

create_lookup_table("OptimizationTypes", optimization_types)
create_lookup_table("ContractStatuses", contract_statuses)
create_lookup_table("CustomerRelevances", customer_relevances)
create_lookup_table("ProgramTypes", program_types)




def get_id_by_description(collection_name, description):
    document = db[collection_name].find_one({"Description": description})
    if document:
        return document["_id"]
    else:
        print(f"Warning: {description} not found in {collection_name} collection.")
        return None  



area_types = {
    "Residential": get_id_by_description("ProgramTypes", "Residential"),
    "Industrial": get_id_by_description("ProgramTypes", "Industrial"),
    "Business": get_id_by_description("ProgramTypes", "Business")
}

customers = []
for i in range(1, 201):
    name = f"Customer_{i}"
    rua_code = f"{i:02}"

    if i <= 67:
        area_type = "Residential"
        postcode = f"8{rua_code}-00{i % 1000:03}"
        mobile_info = f"+3519100{str(i).zfill(4)}"
    elif i <= 134:
        area_type = "Industrial"
        postcode = f"9{rua_code}-00{i % 1000:03}"
        mobile_info = f"+3519200{str(i - 67).zfill(4)}"
    else:
        area_type = "Business"
        postcode = f"7{rua_code}-00{i % 1000:03}"
        mobile_info = f"+3519300{str(i - 134).zfill(4)}"

    full_address = f"rua {i}, Faro"
    relevance_id = get_id_by_description(
        "CustomerRelevances", "High" if i % 3 == 0 else "Medium" if i % 3 == 1 else "Low")

    customer = {
        "Name": name,
        "ConsumerType": area_type,
        "Address": full_address,
        "ContactInfo": mobile_info,
        "RelevanceID": relevance_id,
        "ContractID": f"CT{i:05}",
        "ContractStartDate": datetime(2023, 1, 1) + timedelta(days=i * 10),
        "ContractEndDate": datetime(2025, 1, 1) + timedelta(days=i * 10),
        "ContractCommitment": datetime(2024, 1, 1) + timedelta(days=i * 5),
        "Comments": f"Customer {i} is part of the {area_type} program."
    }
    customers.append(customer)

db.CustomerDetails.insert_many(customers)


policies = []
for i in range(1, 51):
    policy = {
        "PolicyName": f"Policy_{i}",
        "PolicyInfo": f"Details about Policy {i}",
        "PublicationDate": datetime(2022, 1, 1) + timedelta(days=i * 5),
        "EffectiveDate": datetime(2023, 1, 1) + timedelta(days=i * 10)
    }
    policies.append(policy)

db.PoliciesDetails.insert_many(policies)


optimizations = []
for i in range(1, 201):
    optimization = {
        "CustomerID": i,
        "TypeID": get_id_by_description("OptimizationTypes", optimization_types[i % len(optimization_types)]),
        "StartDate": datetime(2023, 1, 1) + timedelta(days=i * 3),
        "ProjectedSavings": float(i * 1.5)
    }
    optimizations.append(optimization)

db.WaterUsageOptimization.insert_many(optimizations)


contract_statuses_data = []
for i in range(1, 201):
    status = {
        "StatusID": get_id_by_description("ContractStatuses", contract_statuses[i % len(contract_statuses)]),
        "OptimizationID": i
    }
    contract_statuses_data.append(status)

db.Customer_ContractStatus.insert_many(contract_statuses_data)


programs = []
for i in range(1, 21):
    program = {
        "ProgramName": f"Program_{i}",
        "TypeID": get_id_by_description("ProgramTypes", program_types[i % len(program_types)]),
        "StartDate": datetime(2023, 1, 1) + timedelta(days=i * 30),
        "EndDate": datetime(2025, 1, 1) + timedelta(days=i * 30),
        "TargetArea": f"Region_{i}"
    }
    programs.append(program)

db.WaterConservationPrograms.insert_many(programs)


participants = []
for i in range(1, 201):
    participant = {
        "CustomerID": i,
        "ProgramID": (i % 20) + 1,
        "ParticipationStartDate": datetime(2023, 1, 1) + timedelta(days=i * 2),
        "BenefitsReceived": f"Benefits for Customer {i} in Program {(i % 20) + 1}"
    }
    participants.append(participant)

db.ConservationParticipants.insert_many(participants)


contract_policies = []
for i in range(1, 201):
    customer_id = i
    policy_ids = [
        get_id_by_description("PoliciesDetails", f"Policy_{(i % 50) + 1}")
    ]


    if any(policy_ids):  
        
        for policy_id in policy_ids:
            if policy_id:  
                contract_policy = {
                    "CustomerID": customer_id,
                    "PolicyID": policy_id,
                    "ContractDate": datetime(2023, 1, 1) + timedelta(days=i * 7),
                    "Status": "Active"
                }
                contract_policies.append(contract_policy)


if contract_policies:
    db.ContractPolicies.insert_many(contract_policies)
else:
    print("No contract policies to insert.")

db.ContractPolicies.insert_many(contract_policies)

print("MongoDB database has been created and populated successfully!")
