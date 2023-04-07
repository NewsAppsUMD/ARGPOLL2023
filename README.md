# ARGPOLL2023
A repository for a web scraper that will scrape poll numbers for the 2023 Argentine General Election
Update: 4/7/2023

FINAL UPDATE :

PLEASE NOTE THAT WHILE GITHUB ACTIONS SAYS THE ACTIONS FAILED, THAT IS NOT CORRECT. THE EMAIL SENDS CORRECTLY. It only has that failiure notification because some of the libraries or actions in the code need to be updated. I tried updating them but that just messes up the code so I left the code as is. Again, the email still sends with the CSV, it is fine. 

Here is the final code for the scrapper for the polls. As you saw in the sample email I sent to you, I did achieve some things and mostly got a scrapper and email notification I wanted. My only regrest is I wasn't able to make the bot aestheitically pleasing. 

The CSV that I was able to make is ok, but is isn't perfect. There are some wonky things on there such as the CSV table not taking into account letters with spanish accent marks on them, and outputs them as weird symbols in the CSV. I tried fixing that, but when I did do that, the scraping would not be able to read or output ANY text onto the CSV, so I therefore just left that alone. Please keep in mind that chat GPT was used to craft the scrape.py and YAML codes, to see interactions I had with it, please refer back to the readme.md in the old repository. But suffice to say, it was basically just me posting codes to it, along with error messages and asking it to fix them. If I had any modificiations I would describe them to it and it would add them to the code. That did help with me getting github secrets and connecting my gmail to actually send and recieve those emails sucesfully.  

Another thing is you can see in the CSV that polls with TWO sets of data have their second set aligned to the left on their rows. Its a problem I tried to fix but ultimately that would cause the whole table to shift over when I tried to fix it, so I lef thtat as is too. 

That was a hard process, but that proved to be actually the easier of the two. Creating the YAML code was easy per say, but it was the contexts of the Email that dissapointed me. In the end this is what the email looks like:

"Hello, 

Enclosed you will find the latest polling results for the 2023 Argentine General Election. Please note these results are only measuring poltical party support and not support for any candidate. These results can therefore be read to signify citizen's voting intentions for the Congressional elections and not the Presidential election.

 Best, 
 -Ryan Mercado
-CSV FILE ATTACHED-

While thats all ok, its not the best it can be. What I wanted to do was to display the CSV results as a table on the email. That proved to be VERY difficult, and no amount of Chat GPT would work. I tried for hours, going through many many Chat GPT chats, asking it things like:

"I have these two codes, I would like for the email outputed from them to take the results from the CSV and present them in the email as a table, can you do that for me?"

And that led me on a rabbit hole of two days, testing code after code, and getting error after error. I did have some success, such as the email eventually displaying a parcel of the code where the table should have been, but I ultimately could not get a working table on there. I tried the Tabulate library, I tried formatting it as an HTML table, I tried other things that I am forgetting becuase there were many attempts, which are reflected in the many commits I did to test, but none worked.

Ideally, this is what I wanted my email to look like with a working table:

"Hello, 

Enclosed you will find the latest polling results for the 2023 Argentine General Election. Please note these results are only measuring poltical party support and not support for any candidate. These results can therefore be read to signify citizen's voting intentions for the Congressional elections and not the Presidential election.


|     Polling firm     |  Date  |   Party A  |   Party B  |   Party C  |
|----------------------|--------|------------|------------|------------|
|   Polling firm 1     | 4/1/23 |     25%    |     30%    |     45%    |
|   Polling firm 2     | 4/5/23 |     20%    |     40%    |     40%    |
|   Polling firm 3     | 4/7/23 |     35%    |     25%    |     40%    |

Best regards,
Ryan Mercado

That is my dream table, and I wasn't able to get it. Don't get me wrong, the CSV file and the little message are ok, but I think for a professional newsroom, the dream email would be better.

So that is where this bot ends. I accomplished most of what I wanted but there is still work to do to make it nicer to look at. I am very happy though I was able to get a working email bot to some extent. 

Does the data need to be stored? Not really, the wikipedia page does a good job at that. I can get any of that data from there.
Can this bot accept input from users? I mean yes, but I am not sure what the criticisms would be aside from that the CSV file looks wonky. Many would want a candidate-centered CSV but that proves very difficult with the way the candidate table is set up on the wikipedia page. I would wait until after the primaries in August when the number of candidates whittles. Whats the best schedule? I put everyday since polls come out nearly every day or every week. I think that suits this. 


<End of update>