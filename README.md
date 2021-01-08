# Plant-App
# Create a virtual environment
  python3.8 -m venv plant-app-venv
  source plant-app-venv/bin/activate
  pip install --upgrade pip

# Activate virtual environment
  source plant-app-venv/bin/activate

# Deactivate virtual envirmonment
  deactivate

#retrieve_data.py
  pip install pandas
  pip install streamlit
  pip install tqdm
  pip install ratelimit


#app.py
  streamlit run app.py

#Uploading to git
  -> Go to plant_app directory
  git add .
  git commit -m "Add existing file"
  git push origin main
