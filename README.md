# Hearthstone Card Display Bot<img src=https://user-images.githubusercontent.com/52103944/163253624-df8fa12e-4d7c-4faf-ab64-22bf934e00d7.png alt="hearthstone emblem" width="50" height="30"/>
A Discord bot to display Hearthstone card images and metadata

## Underlying API
Link to the documentation for the underlying [Hearthstone API](https://rapidapi.com/omgvamp/api/hearthstone/).

If you wish to run this bot locally, you will need to register with RapidAPI to receive an X-RapidAPI-Key.

## How to Use
Inside a discord message within a channel that contains the hs-card-display-bot, enclose the name, partial name, or dbfId of a Hearthstone card in either `[]` or `{}` brackets. 
  - `[CARD_NAME]` will return an image of the card
  - `{CARD_NAME}` will return the metadata of the card in a discord embed

You can have a message that contains multiple brackets of different types
  - E.G - `"[Mr. Smite] in pirate warrior is too strong! I can't win with my {RENO JACKSON} control deck!`

Card names are **NOT** case-sensitive
  - `{Arbor Up}`, `{aRbOr Up}`, `{arbor up}`, `{ARBOR UP}` all fetch and return the same card.

The term card is used loosely, as both bosses from Adventures as well as heroes from Battlegrounds are considered cards in the API.

#### Ambiguous Request
If a request returns more than one possible card, the bot will return a list of card names and dbfIds. You can then enter the dbfId within brackets to fetch the correct card.
  - A request of `[YSERA]` will return 13 card names in the form `name: dbfId` separated by newlines. Five of these cards will be named `Ysera`, the remaining 8 will contain the name `Ysera`. 
    - If the card you were trying to fetch was the original 9 mana 4/12 Ysera, you would then enter a new message with `[1186]` or `{1186}`.
#### Workaround
Given an ambiguously named card, such as five cards with the exact name `Ysera`, to get the dbfId corresponding to the card you're looking for, you can go to https://playhearthstone.com/en-us/cards and search for your card there. When brought to the page for the card, you can extract the dbfId from the url: .../cards/**1186**-ysera?...
 
### Limitations 
- Partial name searches return multiple results and the names do not clearly indicate the actual card it corresponds to. Multiple card objects can share attributes and only the dbfId is considered unique in the underlying API. So, the only way to fetch an ambiguously or non-uniquely named card is to use the dbfId.
  - With this, there is likely a more user-friendly way to handle multiple cards, and that is one of the notable future improvements.   
- There is currently no support for user customization of the bot, but future commands will be added to allow users to configure the bot. 
  - For example, an immediate use case would be to allow users to set whether they wish to filter non-collectible cards, such as Boss cards or Battleground Hero cards.
- The [Hearthstone API](#underlying-api) used by this bot has support for Cardback objects, and the `hearthstone` package also has support for Cardbacks, but there is no code implemented for the bot to handle Cardback requests.
- Nested brackets are considered invalid, and the bot will not process them.
  - E.G - [I LOVE [CARD_NAME]] 

## Future Improvements
- Implement bot commands for bot configuration and usage assistance
- Implement code to fetch Cardback objects
- Improve handling of ambiguous name requests
- Create a standalone library from the hearthstone package
