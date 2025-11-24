import re

def manual_reorder():
    file_path = '/Users/rajattiwari/portfolionew/index.html'
    
    with open(file_path, 'r') as f:
        content = f.read()

    # Find the Everything View container
    start_marker = '<div id="everything-view" class="masonry-grid">'
    # We need to find the end of this div.
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("Could not find #everything-view")
        return

    search_start = start_idx + len(start_marker)
    stack = 1
    current_idx = search_start
    
    while stack > 0 and current_idx < len(content):
        if content[current_idx:current_idx+4] == '<div':
            stack += 1
            current_idx += 4
        elif content[current_idx:current_idx+5] == '</div':
            stack -= 1
            current_idx += 5
        else:
            current_idx += 1
            
    end_idx = current_idx
    grid_content = content[search_start:end_idx-6] # Exclude the last </div>
    
    # Extract cards
    lines = grid_content.split('\n')
    cards = []
    current_card = []
    in_card = False
    card_div_stack = 0
    comment_buffer = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('<!--') and stripped.endswith('-->') and not in_card:
            comment_buffer.append(line)
            continue
        if '<div class="grid-item"' in line:
            in_card = True
            card_div_stack = 1
            current_card.extend(comment_buffer)
            comment_buffer = []
            current_card.append(line)
            continue
        if in_card:
            current_card.append(line)
            card_div_stack += line.count('<div') - line.count('</div')
            if card_div_stack == 0:
                in_card = False
                cards.append('\n'.join(current_card))
                current_card = []
        else:
            pass

    print(f"Found {len(cards)} cards in current file.")

    # Define signatures for the 47 cards in ORIGINAL order (1-47)
    # This maps Index (1-based) -> Unique String in content
    signatures = {
        1: "Engineer, Creative, Tinkerer",
        2: "t9HmOz8H0qI", # Steve Jobs 1983
        3: "Some Work", # Experience
        4: "4065d22b2a8afa97fd9c8069b0ded605.jpg", # Balloon Dog
        5: "mémoire enables any LLM",
        6: "Principles",
        7: "61a9da80-4062-4551-9ccf-4c3fd1d1f575.jpeg", # Curation 3
        8: "b9af4e0c092231d8fc980b296e4d2bf9.jpg", # Virgil Abloh
        9: "88d5401a9d72cf8a0ba8b91ee2796c5c.jpg", # Dieter Rams
        10: "Total LLMification",
        11: "175f88c894906e96dfbe91ac82e49c55.jpg", # SpaceX
        12: "90a9cd7a225be8661aa62dd073936152.jpg", # Curation 6
        13: "Thoughts on Products",
        14: "Flashrpc",
        15: "G4hL5Om4IJ4", # Jim Keller
        16: "21fe12ab8a42ebf7be85a78b54fa8f7c.jpg", # Rubik's Cube
        17: "AE005nZeF-A", # Frank Ocean
        18: "UYXa2yBF5ms", # Kanye I Wonder
        19: "jiHZqamCD8c", # Steve Jobs 2005
        20: "ivCY3Ec4iaU", # Kanye Follow God
        21: "We habituate to everything", # Love and Habituation
        22: "8e6a060ec4a0c53c1dbf645d48896bab.jpg", # MJ
        23: "How I Work",
        24: "107465513d262eb7c77143fcc520b489.jpg", # Curation 1
        25: "af7a27b50143212cf38cdc54ba8499e2.jpg", # Curation 9
        26: "cd98923d9a12a4f19f54d33eb77faaeb.jpg", # Kanye West
        27: "2cda304e-771a-46b2-98fa-22b71c67bc70.jpeg", # Curation 2
        28: "ded89f8d28bd927d3b6cbaf667519605.jpg", # Curation 13
        29: "Thoughts on Design",
        30: "e77a65a2221d9305557e7c589c7554e0.jpg", # Steve Jobs
        31: "Information Topology",
        32: "LCEmiRjPEtQ", # Andrej Karpathy
        33: "LA Shelter Platform",
        34: "DR_yTQ0SYVA", # Kanye Zane Lowe
        35: "af63a64039d2cdc2136c5475f491a95a.jpg", # Curation 8
        36: "d1bb5916-2ae8-4421-9316-667e594cd5fa.jpeg", # Curation 12
        37: "sk3rpYkiHe8", # Kanye Devil
        38: "wiALRpD0Ztg", # Kendrick
        39: "Qz3LK267YVI", # Drake
        40: "V23eW2KEIuU", # Karan Aujla
        41: "owxmFmg5SVk", # Intuitive Machines
        42: "810c69b9-dd3c-4c72-b1ce-94041c7110e5.jpeg", # Curation 4
        43: "85f226ada9cdc724c2b2d8f557899f94.jpg", # Curation 5
        44: "9c67d2a2-d74b-443d-b70a-e5aa0c4cc446.jpeg", # Curation 7
        45: "afd2c0955c31b50a033ecfb0b0ee5916.jpg", # Curation 10
        46: "ce492a1fcfff81c52e64d3b8e48d3df8.jpg", # Curation 11
        47: "Building systems that think alongside humans"
    }

    # Map extracted cards to their original index
    card_map = {} # Index -> Card Content
    
    for card_content in cards:
        found = False
        for idx, sig in signatures.items():
            if sig in card_content:
                if idx in card_map:
                    print(f"Warning: Duplicate card found for index {idx}")
                card_map[idx] = card_content
                found = True
                break
        if not found:
            print(f"Warning: Could not identify card:\n{card_content[:100]}...")

    if len(card_map) != 47:
        print(f"Error: Only identified {len(card_map)}/47 cards. Aborting.")
        missing = set(range(1, 48)) - set(card_map.keys())
        print(f"Missing indices: {missing}")
        return

    # Construct the target sequence
    # Swapped 2 and 3 to put "About Me" (1) and "Some Work" (3) next to each other
    target_sequence = [
        1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45,
        3, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46,
        2, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47,
        4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44
    ]

    new_cards_content = []
    for idx in target_sequence:
        new_cards_content.append(card_map[idx])

    # Reconstruct file
    new_grid_content = '\n\n'.join(new_cards_content)
    new_grid_content = '\n\n' + new_grid_content + '\n\n            '
    
    final_content = content[:search_start] + new_grid_content + content[end_idx-6:]
    
    with open(file_path, 'w') as f:
        f.write(final_content)
        
    print("Successfully manually reordered index.html")

if __name__ == "__main__":
    manual_reorder()
