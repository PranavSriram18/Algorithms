from typing import Dict

class SocialNetworkAnalyzer:

    # Content gap threshold in seconds
    CONTENT_GAP_THRESHOLD = 30 * 24 * 3600.0

    def analyze(self, data: Dict):
        """ 
        data is:
        data -> {user: ..., hashtags: ..., }
        user -> {posts, following, followers}
        posts -> List[Entry]
        Entry: {'id': id, 'likes': likes, 'timestamp': timestamp}
        following -> List[user]
        followers -> List[user]
        """
        self.data = data
        self.run_preprocessing()

        # get 3 most influential users
        users = self.data['users'].keys()
        top_users = sorted(users, key=lambda u: -self.influence(u))[0:3]

        # get trending hashtags
        hashtags = self.data['hashtags'].keys()
        top_hashtags = sorted(hashtags, key=lambda h: -self.hashtag_avg_likes(h))[0:3]

        # get user engagement rate
        engagement_dict = {user : self.engagement(user) for user in users}

        # get content gaps
        content_gaps = [user for user in users if self.has_gap(user)]

        # get collabs
        collabs = None  # TODO - next part

        return {
            'top_influencers': top_users,
            'trending_hashtags': top_hashtags,
            'user_engagement': engagement_dict,
            'content_gaps': content_gaps,
            'potential_collaborations': collabs
        }

    def run_preprocessing(self):
        user_data = self.data['users']
        # build post -> likes and user -> total likes
        self.post_to_likes = dict()
        self.user_total_likes = dict()
        for user, user_map in user_data.items():
            self.post_to_likes |= {entry['id'] : entry['likes'] for entry in user_map['posts']}
            self.user_total_likes[user] = sum(entry['likes'] for entry in user_map['posts'])

        # get last timestamp
        timestamps = [entry['timestamp'] for entry in [v['posts'] for v in user_data.values()]]
        self.last_timestamp = max(timestamps)

    def influence(self, user: str) -> float:
        user_data = self.data['users'][user]
        num_posts = len(user_data['posts'])
        num_followers = len(user_data['followers'])
        num_likes = self.user_total_likes[user]
        return 0.5 * num_likes + 0.3 * num_followers + 0.2 * num_posts
    
    def hashtag_avg_likes(self, hashtag: str) -> float:
        posts = self.data['hashtags'][hashtag]
        return sum(self.post_to_likes[post] for post in posts) / len(posts)
    
    def engagement(self, user: str) -> float:
        user_data = self.data['users'][user]
        return (self.user_total_likes[user] / len(user_data['followers'])) / len(user_data['posts'])

    def has_gap(self, user: str) -> bool:
        user_timestamps = [entry['timestamp'] for entry in self.data['users'][user]['posts']]
        return self.last_timestamp - max(user_timestamps) >= SocialNetworkAnalyzer.CONTENT_GAP_THRESHOLD
