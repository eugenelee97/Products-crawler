# ProductsCrawler-Shopee.com

This is personal project for personal uses, still wroking on this project.


#### ReadURL
- Crawling specific products user wants and get url address with using **Selenium**. 
**Shopee API** is used to get seller name, and other info of products.
Results will be exporting to csv file. 

#### CheckURL
- Search for duplicated url on groupware website, 
comparing URLs in csv to all URLs on dashboard people'd uploaded before. 


#### UploadURL
- Upload all those unposted URL I want to uploard with given product's code on the dashboard


## Installation

This project requires **Python v.3+** to run.
Make sure you have updated python.

```sh
python --version
```

## Development

Want to contribute? Great!

Open your terminal and run these following commands.

ReadURL:
```sh
cd filelocation
python ReadURL keyword(ex.Tobot) pagenumber(ex.33)
````

(-) Due to privacy issue, won't be able to contribtue on these two files. 

CheckURL, UploadURL:
```sh
cd filelocation
python CheckURL/UploadURL filename(csv format)
```
