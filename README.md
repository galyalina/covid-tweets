# COVID-Tweets

The application reads tweets from a simulated TCP stream, processes them, fetches COVID-19 statistics, and stores the combined data in a MongoDB database. The project is structured into two main parts: the Apache Beam application and the TCP stream simulator.

## How to Run Locally

```sh
docker-compose build
docker-compose up
```

This will start the following services:

- **mongodb**: A MongoDB instance to store the processed data.
- **twitter-simulator**: A TCP server that simulates a stream of tweets.
- **beam-app**: An Apache Beam application that processes tweets and fetches COVID-19 statistics.

The code is structured into modular components such as ReadFromTCP, CleanTweet, FetchCovidStats, and SaveToMongoDB, which can be easily extended or replaced.

### Suggested Extensions

- **Introduce a fallback**: If fetching live COVID-19 statistics fails, the system should use the most recent successful fetch stored locally or in a cache.
- **Error Handling**: Manage errors in a separate collection to facilitate retry logic, error logging, or other actions, ensuring that the main processing pipeline remains unobstructed.