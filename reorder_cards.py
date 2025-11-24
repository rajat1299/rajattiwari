import re

def reorder_cards():
    file_path = '/Users/rajattiwari/portfolionew/index.html'
    
    with open(file_path, 'r') as f:
        content = f.read()

    # Find the Everything View container
    start_marker = '<div id="everything-view" class="masonry-grid">'
    end_marker = '<!-- CURATION IMAGE 4 -->' # Just a temporary marker to find the end, but better to find the closing div
    
    # Locate the start index
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("Could not find #everything-view")
        return

    # Find the end of the div. Since we know the indentation, we can look for the closing div at the same level.
    # The start tag is at a certain indentation. The closing tag should match.
    # Let's look at the file content again. Line 175 is the start. Line 1263 is the end.
    # We can just extract the substring between these known lines or find the matching closing div.
    
    # Let's use a stack to find the matching closing div for robustness
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
    
    # Now parse the cards from grid_content
    # Each card block typically starts with a comment or the div.
    # We'll split by the pattern that matches the start of a card block.
    # Most cards start with "<!-- ... -->\n            <div class="grid-item"..."
    # Some might just start with <div class="grid-item"
    
    # We will iterate through the lines to build card blocks
    lines = grid_content.split('\n')
    cards = []
    current_card = []
    in_card = False
    card_div_stack = 0
    
    # Buffer for comments preceding a card
    comment_buffer = []
    
    for line in lines:
        stripped = line.strip()
        
        # Check for comment
        if stripped.startswith('<!--') and stripped.endswith('-->') and not in_card:
            # Check if it's a card comment (heuristic: usually uppercase or specific format, but let's just keep all comments that precede a grid-item)
            # However, we must be careful not to capture comments that are inside the previous card (but we are !in_card)
            comment_buffer.append(line)
            continue
            
        # Check for start of grid item
        if '<div class="grid-item"' in line:
            in_card = True
            card_div_stack = 1
            # Start a new card block with the buffered comments
            current_card.extend(comment_buffer)
            comment_buffer = []
            current_card.append(line)
            continue
            
        if in_card:
            current_card.append(line)
            # Track div nesting to find end of grid-item
            card_div_stack += line.count('<div') - line.count('</div')
            
            if card_div_stack == 0:
                in_card = False
                cards.append('\n'.join(current_card))
                current_card = []
        else:
            # Empty lines or whitespace between cards
            if not stripped:
                continue
            # If there's content that's not a comment and not a grid-item start, it's weird.
            # But looking at the file, it's mostly clean.
            pass

    print(f"Found {len(cards)} cards.")
    
    # Reorder logic
    # We want visual row-by-row filling.
    # Current HTML fills Col 1, then Col 2, etc.
    # We want to redistribute the CURRENT cards (which are 1..47) such that:
    # Col 1 gets: 1, 5, 9...
    # Col 2 gets: 2, 6, 10...
    # etc.
    
    num_columns = 4
    new_cards = []
    
    # Create the 4 columns lists
    columns = [[] for _ in range(num_columns)]
    
    # Distribute cards into columns (1, 2, 3, 4, 1, 2, 3, 4...)
    # This effectively does the "take every 4th card" logic
    # Wait, if we want the RESULT to be 1, 2, 3, 4 across the top...
    # And the browser fills Col 1 first...
    # Then Col 1 MUST contain cards 1, 5, 9...
    # So we need to construct the new HTML list by concatenating:
    # [Cards for Col 1] + [Cards for Col 2] + ...
    
    # The cards for Col 1 are indices 0, 4, 8... (0-indexed)
    # The cards for Col 2 are indices 1, 5, 9...
    
    for col in range(num_columns):
        # Get every 4th card starting from col index
        col_cards = cards[col::num_columns]
        new_cards.extend(col_cards)
        
    print(f"Reordered {len(new_cards)} cards.")
    
    # Reconstruct the content
    # Join with newlines and ensure proper indentation
    new_grid_content = '\n\n'.join(new_cards)
    
    # Add some padding newlines
    new_grid_content = '\n\n' + new_grid_content + '\n\n            '
    
    # Replace in original content
    final_content = content[:search_start] + new_grid_content + content[end_idx-6:]
    
    with open(file_path, 'w') as f:
        f.write(final_content)
        
    print("Successfully updated index.html")

if __name__ == "__main__":
    reorder_cards()
