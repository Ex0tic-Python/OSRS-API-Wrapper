from string import ascii_lowercase
from requests import get
from json import dump
from time import perf_counter
from traceback import print_exc

def debug_refresh_json_table():
    start_time = perf_counter()
    final_table_json = {}
    
    # Iterates over all letters
    for letter in ascii_lowercase:
        print(f"Started letter iteration loop with letter \"{letter}\" ({round(perf_counter() - start_time, 2)}s)")
        
        # iterates over all the pages of the letter
        i = 0
        while i := i + 1: # Infinite auto-incrementing loop
            print(f"Started page iteration loop with increment value \"{i}\" ({round(perf_counter() - start_time, 2)}s)")
            
            # Get response and verify it's valid
            while True:
                itemdb_response = get(f"https://secure.runescape.com/m=itemdb_oldschool/api/catalogue/items.json?category=1&alpha={letter}&page={i}")
                print(f"Recieved OSRS API Response ({round(perf_counter() - start_time, 2)}s)")
                if itemdb_response.status_code != 200:  # Response should always be 200 if everything went fine
                    ################################################################################raise UnexpectedStatusCodeRecieved(itemdb_response.status_code, "200")
                    raise f"Status Code \"{itemdb_response.status_code}\" recieved; Expected 200"
                print(f"Response Status Code recieved was 200 ({round(perf_counter() - start_time, 2)}s)")
                # For some reason, request occasionally returns an empty byte string. Check for it and remake request
                if itemdb_response.content == b"":
                    print(f"Response Content was an empty byte string. Making new API Request ({round(perf_counter() - start_time, 2)}s)")
                    continue
                break
            
            # Verify that items list isn't empty
            itemdb_json = itemdb_response.json()
            print(f"Converted Response to JSON Data with an \"items\" list length of \"{len(itemdb_json['items'])}\" ({round(perf_counter() - start_time, 2)}s)")
            if itemdb_json["items"] == []:
                print(f"JSON \"items\" list evaluated to an empty list. Now exiting loop with letter \"{letter}\" and increment \"{i}\" ({round(perf_counter() - start_time, 2)}s)")
                break  # Breaks from infinite while loop and iterates over a new letter
            
            # Save all elements on the page then restart loop with +1 increment
            for item in itemdb_json["items"]:
                final_table_json[item["name"]] = item["id"]
                print(f"Saved Item \"{item['name']}\" with ID \"{item['id']}\" ({round(perf_counter() - start_time, 2)}s)")
    
    # Open JSON file, clear it, and save the new data
    with open("id_table.json", "w") as json_file:
        print(f"Opened JSON file successfully and will now attempt to write all data to it ({round(perf_counter() - start_time, 2)}s)")
        dump(final_table_json, json_file, indent = 4)
        print(f"Successfully wrote all data ({round(perf_counter() - start_time, 2)}s)")
    
    # If everything went fine, return None
    return None

# Include the ability to run a special variation of refresh_json_table() for debugging purposes
if __name__ == "__main__":
    start_time = perf_counter()
    try:
        print("Initializing refresh_json_table()" + "\n\n" + "-" * 20 + "\n")
        return_value = debug_refresh_json_table()
        print("\n" + "-" * 20 + "\n")
        print(f"refresh_json_table() returned \"{return_value}\" of type \"{type(return_value)}\"")
        print(f"Finished clearing and updating JSON in ~{round(perf_counter() - start_time, 2)} seconds")
    except Exception as err:
        print("\n" + "-" * 20 + "\n")
        print("Error raised:\n\n")
        print(print_exc())
