# Testing

## NavBar

On the navbar the user sees the following links:

- Home
- Enemy Index
- Stage Index
- Statistics

All the routes work accordingly:

- Click on home link, or the site logo, takes you to route '/home'
- Click on enemy index link to route '/enemy-index'
- Click on stage index link to route '/stage-index'
- Click on statistics link to route '/statistics'

## Footer

On the footer I tested the following:

1. Click on the GitHub logo to verify that a new tab containing my GitHub profile opens up.
2. Click on the LinkedIn logo to verify that a new tab containing my LinkedIn profile opens up.

## Home Page(/home)

On the home page the following was tested:

1. Click on the AppStore banner to verify that a new tab containing the games AppStore page opens up.
2. Click on the GooglePlay banner to verify that a new tab containing the games GooglePlay page opens up.

## Enemy Index(/enemy-index)

On the enemy index the following was tested:

1. Click on the enemy portrait to verify that the user is taken to that specific enemies more info page.
2. Click on the more info icon to verify that the user is taken to that specific enemies more info page.
3. Entering an empty, or less than two characters, search bar pops up a message telling the user that more than two characters are needed in order to search.
4. Click on the message to hide it.
5. Entering a combination of characters return the index filtered by said characters.
6. Entering a combination of characters which don't exist in the database return the index with a no results found message.
7. Click on the filter button to open the filter menu.
8. Click on the close button in the filter menu to close the filter menu.
9. Click on any of the filters to select a filter.
10. Click on clear to remove any selected filters.
11. Click on submit, with or without any filters, returns the index with said filters in place.
12. Click on the reset button to return the index to its original state.
13. Click on the pagination numbers, or arrow, to go to a specific page.

## More Info <Enemy>(/enemy-index/<enemy_code>)

On the more info enemy the following was tested:

1. Click on the arrow in the top right to go back to the previous page.
2. Click on a stage name for the user to be taken to that specific stages more info page.
3. Trying to do an SQL Injection, typing a new code in the search bar, takes the user to a 404 page.

## Stage Index(/stage-index)

On the stage index the following was tested:

1. Click on the more info icon to verify that the user is taken to that specific stages more info page.
2. Entering an empty, or less than two characters, search bar pops up a message telling the user that more than two characters are needed in order to search.
3. Click on the message to hide it.
4. Entering a combination of characters return the index filtered by said characters.
5. Entering a combination of characters which don't exist in the database return the index with a no results found message.
6. Click on the reset button to return the index to its original state.
7. Click on the select menu to filter the index by in which episode the stages appear in.
8. Selecting an option from the select menu automatically filters the index.
9. Click on the pagination numbers, or arrow, to go to a specific page.

## More Info <Stage>(/stage-index/<stage_code>)

On the more info stage the following was tested:

1. Click on the arrow in the top right to go back to the previous page.
2. Click on the enemy portrait or more info button for the user to be taken to that specific enemies more info page.
3. Trying to do an SQL Injection, typing a new code in the search bar, takes the user to a 404 page.

## Statistics(/statistics)

On the statistics page the following was tested:

1. Click on the select menu to filter the index by in which episode the stages appear in.
2. Selecting an option from the select menu automatically filters the charts.
