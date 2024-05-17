#pragma once

#include <string>
#include <queue>
#include <vector>
#include <set> 

#include <stdio.h>
#include <curl/curl.h>

/**
 * Scratch
 * Traverse a website
 * Gather its links
 * 
 * Seed link: https://www.pluralsight.com/
 * 
*/


class WebCrawler {
public:
    WebCrawler(std::string seedLink) {
        seedLink_ = seedLink;
        initQueue();
        processQueue();
        return extLinks_;
    }


private:
    void initQueue() {
        std::string siteMap = seedLink_ + "/sitemap.xml";
        std::string siteMapPayload = getPayload(siteMap);
        parsePayload(siteMapPayload);
    }

    void processQueue() {
        std::string currSite = q_.front();
        std::string currPayload = getPayload(currSite);
        q_.pop();
        std::vector<std::string> links = getLinks(currPayload);
        for (const auto& link : links) {
            auto [internal, normalizedLink] = isInternal(link);
            if (internal) {
                if (intLinks_.count(normalizedLink)) continue;
                intLinks_.insert(normalizedLink);
                q_.push(normalizedLink);
            } else {
                extLinks_.insert(normalizedLink);
            }
        }
    }

    // Get links from xml and seed queue
    void parsePayload(const std::string& payload) {
        int pos = 0;
        int n = payload.size();
        while (pos < n) {
            int locStart = payload.find("<loc>", pos);
            if (locStart == std::string::npos) break;

            int urlStart = locStart + 5;
            int locEnd = payload.find("</loc>", urlStart);

            std::string url = payload.substr(urlStart, locEnd - urlStart);
            q_.push(url);
            pos = locEnd + 6;
        }
    }

    // Get links from html
    std::vector<std::string> getLinks(const std::string& payload) {
        std::vector<std::string> result;

        int pos = 0;
        int n = payload.size();
        while (pos < n) {
            int locStart = payload.find("<a href=\"", pos);
            if (locStart == std::string::npos) break;

            int urlStart = locStart + 9;
            int locEnd = payload.find("\"", urlStart);

            std::string url = payload.substr(urlStart, locEnd - urlStart);
            result.push_back(url);
            pos = locEnd + 1;
        }
        return result;
    }

    std::string getPayload(const std::string& url) {
        CURL *curl;
        CURLcode res;
        
        curl_global_init(CURL_GLOBAL_DEFAULT);
        
        curl = curl_easy_init();
        if(curl) {
            curl_easy_setopt(curl, CURLOPT_URL, siteMap);
        }

        /* cache the CA cert bundle in memory for a week */
        curl_easy_setopt(curl, CURLOPT_CA_CACHE_TIMEOUT, 604800L);
    
        /* Perform the request, res gets the return code */
        res = curl_easy_perform(curl);
        /* Check for errors */
        if(res != CURLE_OK)
        fprintf(stderr, "curl_easy_perform() failed: %s\n",
                curl_easy_strerror(res));
    
        /* always cleanup */
        curl_easy_cleanup(curl);
        return "";  // TODO
    }

    // Return <isInternal, normalizedLink>
    std::pair<bool, std::string> isInternal(const std::string& link) {
        if (link.size() == 0) return {false, link};
        if (link[0] == "/") {
            return {true, seedLink_ + link};
        }
        if ((link.find(seedLink_), 0) == 0) return {true, link};
        return {false, link};
    }

    std::string seedLink_;

    // Frontier of links to traverse
    std::queue<std::string> q_;

    std::set<std::string> intLinks_;

    std::set<std::string> extLinks_;


};   // class Essential
