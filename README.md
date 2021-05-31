https://discord.com/api/oauth2/authorize?client_id=824630583278960700&permissions=3627547760&scope=bot
# Money Bot
<!-- ABOUT THE PROJECT -->
## About The Project

![project screenshot](https://github.com/JuanSamuel1/Money-Bot/blob/master/money-bot.PNG)

When I saw a music bot in Discord, I thought it will be fun if I can make one. So, I decided to learn more about how to make a bot in discord and tried to make one. I stumbled in 2 choices, either using the discord package in Javascript or the discord package in Python. Since I am more comfortable in using Python, I decided to make it using Python. I tried to find many resources about the discord.py package until I finally felt ready to begin.

Making a discord bot is not easy as you imagine, however, the API provided by Discord for developers surely make it easier. I started plan on how am I gonna make the bot behave as well as created the structure of the bot. After that, I created the function one by one until it behave as I wanted. After I finished creating it, I asked my friend to give it a try and found out that there are still many flaws and bugs in the bot. I patiently fixed the bugs and added new features to it. 

After all the ups and downs, I proudly present to you, the Money Bot.

You can see the demo of the microservice in this link: https://timestamp-microservice-juan.glitch.me

The API will work like the following:
* A request to /api/:date? with a valid date should return a JSON object with a unix key that is a Unix timestamp of the input date in milliseconds
* A request to /api/:date? with a valid date should return a JSON object with a utc key that is a string of the input date in the format: Thu, 01 Jan 1970 00:00:00 GMT
* A request to /api/1451001600000 should return { unix: 1451001600000, utc: "Fri, 25 Dec 2015 00:00:00 GMT" }
* If the input date string is invalid, the api returns an object having the structure { error : "Invalid Date" }
* An empty date parameter should return the current time in a JSON object with a unix key
* An empty date parameter should return the current time in a JSON object with a utc key

It is a very simple API, however, from this project I learned about how to handle GET request and intertwined between unix and utc date format.

It's exciting as well as interesting to build this microservice.That's why I want to share this project here, hope you get some lesson from the code 😄.

### Built With

Here is the list of major frameworks used to built the project.
* [Node JS](https://nodejs.org/en/)

<!-- GETTING STARTED -->
## Getting Started

This is how set up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

Here is the prerequisites of the project.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/JuanSamuel1/Timestamp-Microservice.git
   ```
2. Install NPM packages
   ```sh
   npm install
   ```
