

with open("stc_telco_cloud.csv", "r") as bgp_csv_file:
    lines = bgp_csv_file.readlines()
    
    
    
part_list = []    
    
for line in lines:
    data = line.rstrip().split(",")
    part_list.append(data[2])
    
    
    
final_list = []
  
for part in part_list:
    if part not in final_list:
        final_list.append(part)
        
        
        
print(final_list)
print(len(final_list))    


with open("Parts/stc_telco_cloud_parts.txt", "w+") as f:
    for item in final_list:
        f.write(item + "\n") 
