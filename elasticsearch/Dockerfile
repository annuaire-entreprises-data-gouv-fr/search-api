FROM docker.elastic.co/elasticsearch/elasticsearch:7.17.9

# Check if plugin exists before removing it
RUN if [ $(bin/elasticsearch-plugin list) == "analysis-icu" ]; then elasticsearch-plugin remove analysis-icu; else echo "plugin analysis-icu does not exist!"; fi
RUN elasticsearch-plugin install analysis-icu
