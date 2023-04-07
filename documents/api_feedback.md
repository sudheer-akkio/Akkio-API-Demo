# Feedback

## Enhancements
- GET method on flow (or model) to return response that includes all meta data contained in the insights report (e.g., field importance, data story, precision/recall, etc...). Currently the only way to return the insights report meta data is through the akkio.create_model() method, which should not be the only method that returns this
- When a new CDP or data cleaning step is performed on the dataset, a new dataset gets created with unique dataset id. When returning all datasets using the get_datasets() method, there is no documentation on which dataset version corresponds to a dataset id. It would be nice to have a timestamp, or version, in the dataset response that can help the user know which dataset version corresponds to which ID. 
- create_model() method doesn't allow a way to query the status of training. Requesting a way to query this as I believe the training is async
- Clarify that the ID associated with get_models() output is actually the Flow ID (not a unique model id)


## Bugs
- Models created through the API shows up in the Teams list of flows (e.g., API Flows), but you cannot click into the flow
