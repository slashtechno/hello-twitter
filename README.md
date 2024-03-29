# hello-twitter  
A simple Twitter bot made with Python  

### What it does  
1. Looks for tweets that mention a user.  
2. Scans through the last 20 mentions for #HelloWorld  
3. If the mention contains #TeamSeas, it replies to the mention with the pounds of trash removed by [#TeamSeas](https://teamseas.org)  
4. If the mention contains #HelloWorld, it replies to that tweet with `hi`  

### Setup  

#### Twitter developer account setup  
For this to work, you need to have a Twitter developer account.  
1. To get a developer account, follow [this](https://www.youtube.com/watch?v=iff0ztwErA8) tutorial.   
2. After getting a  developer account, you need to create a project and an app  
3. To generate the keys, go to the app you created and go to `Keys and tokens`  

#### Program Setup  
##### Install dependencies  
###### May need to use pip3  
`pip install -r requirements.txt`  
Create a file in the same folder as `hello-twitter.py` named `.env` and configure it as follows, then run the program (or you can use enviroment variables)  
```
CONSUMER_KEY = "Your consumer key"
CONSUMER_SECRET = "Your consumer secret"
ACCESS_KEY = "Your access key"
ACCESS_SECRET = "Your access secret"
```  
If you want to run this as a service edit the configuration of `hello-twitter.service` to your needs    
Then copy to `/etc/systemd/system/`  
### Roadmap  
- [X] Instead of storing keys in `config.py` store in ~~JSON~~ enviroment variables and `.env`    
- [ ] Allow bot to scrape webpages and answer questions  
      ~~For example, getting the amount of pounds of trash removed by #TeamSeas.~~ DONE! (not with webscraping, downloading json instead)  
- [ ] Have a help command  

#### One more thing  
If you find any bugs, please create a Github issue to report the bug so it can be fixed.  
