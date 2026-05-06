# Thefts in Chicago Prediction Web App

The Web App that predicts thefts in Chicago with no warranty at all.

## Requirements

You can check out about it [here](../Deployment/README.md) from the Deployment folder of the repository.

## Data Files

There are data files required to make the app function. You'll be lead to create them when running the app. These files are not uploaded to GitHub to save space. You can delete them, and let the app regenerate if you like it.

- Dataframes are stored in ./DataFrames
- Prepared Graphs are stored in ./PreparedGraphs
- Test files are stored in ./Test

## Run the App

When requirements meet, you can enter this in terminal:

`streamlit run app.py`

Config file are stored in ./.streamlit/. The port number was set to 18501. You may change it by your wish.

## Notes

- Streamlit reruns every single lines of code when st widgets' statuses change
- You can put variables inside the dict `st.session_state`
- When it reruns, threads are reasigned. Threads are not fixed.
- `st.session_state` is independent in each session (browser tab)
- `st.cache_data` can be used to reduce memory usage across multiple sessions
- About [CSS hacking](https://discuss.streamlit.io/t/css-hacks-for-the-dumb/14501/3)
- About [Pydeck](https://deckgl.readthedocs.io/en/latest/layer.html)
