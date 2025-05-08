import requests
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP(name="Reading Bin Collections Tool", dependencies=["requests"], log_level="INFO")

def format_address(address):
    """
    Format an address string to match the Reading API format.
    Example: "51 Gosbrook Road" -> "51, Gosbrook Road,"
    """
    # Remove any existing commas and extra spaces
    address = address.strip().replace(',', '')
    
    # Split into house number and street name
    parts = address.split(' ', 1)
    if len(parts) != 2:
        return address.upper()
    
    house_number, street = parts
    # Handle house numbers with letters (e.g., 3A)
    return f"{house_number}, {street.upper()},"

def find_uprn(postcode, address):
    """
    Call the Reading API to get all addresses for a postcode,
    then return the AccountSiteUprn for the matching address.
    """
    # Format the address before searching
    formatted_address = format_address(address)

    url = f"https://api.reading.gov.uk/rbc/getaddresses/{postcode}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    
    if not data or 'Addresses' not in data:
        raise ValueError(f"No address data found for postcode '{postcode}'")
    
    addresses = data['Addresses']
    print(f"Found {len(addresses)} addresses for postcode '{postcode}'")

    # Try to find the address you passed in
    address_lower = formatted_address.lower()
    for entry in addresses:
        site_address = entry.get('SiteShortAddress', '')
        if site_address.lower().find(address_lower) != -1:
            uprn = entry.get('AccountSiteUprn')
            if uprn:
                print(f"Found matching address: {site_address}")
                return uprn
            
    # If we get here, no match was found
    print("Available addresses:")
    for entry in addresses:
        print(f"- {entry.get('SiteShortAddress')}")
    raise ValueError(f"No matching address found for '{address}' in postcode '{postcode}'")

def fetch_collections_by_uprn(uprn):
    """
    Call the Reading API to get collection dates for a given UPRN.
    """
    url = f"https://api.reading.gov.uk/api/collections/{uprn}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

@mcp.tool()
def get_collection_dates(postcode: str, address: str):
    """
    Fetch bin collection dates for the given address in the specified postcode.
    """
    print(f"Fetching collection dates for postcode '{postcode}' and address '{address}'")
    uprn = find_uprn(postcode, address)
    return fetch_collections_by_uprn(uprn)

if __name__ == "__main__":
    # Run MCP server over stdio for Claude compatibility
    mcp.run(transport="stdio")
