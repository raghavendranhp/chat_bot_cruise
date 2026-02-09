import pandas as pd
import os
from src.models import CruiseSearchQuery


_DF_CACHE = None
CSV_PATH = os.path.join("data", "structured", "Egypt_Cruise_Dataset.csv")

def load_data():
    """
    Loads CSV into a Pandas DataFrame.
    """
    global _DF_CACHE
    if _DF_CACHE is not None:
        return _DF_CACHE
    
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"CSV not found at {CSV_PATH}")
        
    try:
        df = pd.read_csv(CSV_PATH)
        
        df.columns = df.columns.str.strip()
        _DF_CACHE = df
        return df
    except Exception as e:
        print(f" Error loading CSV: {e}")
        return None

def perform_search(criteria: CruiseSearchQuery):
    """
    The Core Logic: Filters the DataFrame based on the JSON criteria.
    Returns: A string representation of the matching rows (for the LLM to read).
    """
    df = load_data()
    if df is None:
        return "Error: Database not available."

    print(f" Searching CSV with criteria: {criteria.dict(exclude_none=True)}")
    
    #Start with all data
    results = df.copy()

   
    
    #filter by region
    if criteria.cruise_type:
       
        results = results[results['Cruise_Type'].str.contains(criteria.cruise_type, case=False, na=False)]

    #filter by budget
    if criteria.min_budget:
        results = results[results['Price_Per_Person_USD'] >= criteria.min_budget]
    if criteria.max_budget:
        results = results[results['Price_Per_Person_USD'] <= criteria.max_budget]

   
    if criteria.min_duration:
        results = results[results['Duration_Days'] >= criteria.min_duration]
    if criteria.max_duration:
        results = results[results['Duration_Days'] <= criteria.max_duration]


    if criteria.destinations:
        for dest in criteria.destinations:
            
            results = results[results['Destinations'].str.contains(dest, case=False, na=False)]

    
    if criteria.sort_by == "price_asc":
        results = results.sort_values(by="Price_Per_Person_USD", ascending=True)
    elif criteria.sort_by == "price_desc":
        results = results.sort_values(by="Price_Per_Person_USD", ascending=False)
    elif criteria.sort_by == "duration_desc":
        results = results.sort_values(by="Duration_Days", ascending=False)

    
    if results.empty:
        return "No cruises found matching these exact criteria."

    
    top_results = results.head(5)
    
   
    return top_results.to_string(index=False)


if __name__ == "__main__":
    
    test_query = CruiseSearchQuery(
        intent="recommendation",
        max_budget=1600,
        cruise_type="Nile",
        sort_by="price_asc"
    )
    
    print("\n DATABASE RESULTS ")
    print(perform_search(test_query))