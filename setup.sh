mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"anup@ta-dadata.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml