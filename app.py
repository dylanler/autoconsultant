def get_location_data(search_term, location):
    # First, we get the latitude and longitude coordinates of the location
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": location,
        "key": GOOGLE_MAPS_API
    }
    response = requests.get(url, params=params)
    location_data = response.json()["results"][0]["geometry"]["location"]
    
    # Next, we use the Places API nearbysearch endpoint to find places matching the search term
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{location_data['lat']},{location_data['lng']}",
        "radius": "10000", # 5km radius
        #"type": search_term,
        "keyword" : search_term,
        "key": GOOGLE_MAPS_API
    }
    response = requests.get(url, params=params)
    results = response.json()["results"]
    
    # We only want the first 5 results
    results = results[:5]
    
    # For each result, we get the place details to retrieve the description and top reviews
    locations = []
    for result in results:
        place_id = result["place_id"]
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            "place_id": place_id,
            "fields": "name,formatted_address,formatted_phone_number,rating,review",
            "key": GOOGLE_MAPS_API
        }
        response = requests.get(url, params=params)
        place_details = response.json()["result"]
        
        # Create a dictionary representing the location and add it to the list
        location_dict = {
            "name": place_details["name"],
            "address": place_details["formatted_address"],
            #"phone_number": place_details.get("formatted_phone_number", "N/A"),
            #"rating": place_details.get("rating", "N/A"),
            "reviews": []
        }
        
        # Add the top 3 reviews to the dictionary
        reviews = place_details.get("reviews", [])
        for review in reviews[:3]:
            review_dict = {
                #"author": review["author_name"],
                #"rating": review["rating"],
                "text": review["text"],
                #"time": review["relative_time_description"]
            }
            location_dict["reviews"].append(review_dict)
        
        locations.append(location_dict)
    
    return locations

# Define the function to be used in the Gradio app
def find_competitors(product, location):
    locations = get_location_data(product, location)
    if len(locations) == 0:
        return f"No competitors found for {product} in {location}."
    
    output_str = f"Top competitors for {product} in {location}:"
    for i, loc in enumerate(locations):
        output_str += f"\n{i+1}. {loc['name']}"
        output_str += f"\nAddress: {loc['address']}"
        #output_str += f"\nPhone number: {loc['phone_number']}"
        #output_str += f"\nRating: {loc['rating']}"
        output_str += f"\nTop 3 reviews:"
        for review in loc['reviews']:
            output_str += f"\n- {review['text']}"
            #output_str += f"\n  Author: {review['author']}"
            #output_str += f"\n  Rating: {review['rating']}"
            #output_str += f"\n  Time: {review['time']}"
            
    output_str2 = f"Top competitors for {product} in {location}:"
    for i, loc in enumerate(locations):
        output_str2 += f"\n{i+1}. {loc['name']}"
        output_str2 += f"\nAddress: {loc['address']}"
    
    #return output_str

    prompt_input = '''

    You are an expert management consultant that rivals the best of Mckinsey, Bain, BCG.
    The client wants to sell {} in {}.

    {}

    Provide an analysis of the following:

    - Derive insights from the competition and reviews about its products and come up with creative insights that the client execute as part of a differentiating business strategy.
    - From there, think step by step, explain 5 strategies in bullet points of a creative and effective business plan.
    - Suggest a location for the client and explain the rationale of this location step by step.

    '''.format(product, location, output_str)

   
    template = '''
    {history}
    {human_input}
    '''
    prompt = PromptTemplate(
        input_variables=["history", "human_input"], 
        template=template
    )

    chatgpt_chain = LLMChain(
        llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5,openai_api_key=OPENAI_API_KEY), 
        prompt=prompt, 
        verbose=True, 
        memory=ConversationBufferWindowMemory(k=10),
    )

    output = output_str2 + chatgpt_chain.predict(human_input=prompt_input)
    
    return(output)

# Create the Gradio app interface
inputs = [
    gr.inputs.Textbox(label="Product to sell"),
    gr.inputs.Textbox(label="Location")
]


output = gr.outputs.Textbox(label="Business Plan")

interface = gr.Interface(fn=find_competitors, inputs=inputs, outputs=output, title="Auto Consultant", 
             description="Enter a product and a location to find competitors.")
interface.launch()
