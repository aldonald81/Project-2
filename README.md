# Bot Tender

## Developer's Statement
Bot Tender is your personal bartender that is a bot. Bot Tender allows you to speak to it, describing the type of drink you would like to make and any specific ingredients you would like to include. For example, I may ask Bot Tender: "Make me a drink for a hot summer day that is very refreshing and includes vodka" and it returns the Sunrise Refresher with the list of ingredients and how to mix the drink. This tool utilizes a raspberry pie to support a button to trigger recording, an led to let the user know when it is recording, and a python script calling APIs and processing information. Several key APIs used are the google speech to text API to translate the user's audio input to text, the OpenAi API to curate a drink based off the input text, and the Twilio API to send the recipe and directions via text. The most difficult part of this project was piecing the API requests together since each depends on the one before it. This was my project with no utility, providing users with a fun tool to play around with. The flexibility of GPT allows users to prompt Bot Tender with nearly any prompt and still receive a drink recipe. When testing in class, someone said "Give me a drink that includes mayo and ham" and received a Ham Delight incorporating these ingredients along with others. I beleive this project could have significant potential in helping people curate drinks with ingredients that they have, or be more creative in the ingredients they buy and drinks they create.
[Video Demo](https://drive.google.com/file/d/1P-1l7Qq2lKfy6Uv3uEWCv2UK085mFhAu/view?usp=sharing)



## Hardware Components
- Button
    - Begins and ends recording
- LED
    - Lets the user know when the device is recording
- Microphone
    - Records user input audio



## Software Components
- OpenAI GPT API
    - Used to curate a drink based off a prompt that contains the user's drink requests
- Google's Speech Recognition API
    - Tranlates audio to text
- Twilio
    - Send text messages with custom content

## Development Process
[Link to Dev Log](https://docs.google.com/document/d/102Un0wA5PAx8WMP2xizA6PiWHbftrRQiRD14P6ymWI4/edit?usp=sharing)

