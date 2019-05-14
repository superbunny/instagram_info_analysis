from instaloader import Instaloader, Profile
import datetime
import pandas as pd 

account_list = ["uber","lyft"] #sample account
postinfo_list=[]
comment_list=[]
profileinfo_list=[]

for ids in account_list:
    PROFILE=ids
    L = Instaloader(download_videos=False, download_video_thumbnails=False, filename_pattern=ids+"_{date_utc}_UTC",
                    download_geotags=False,download_comments=False,save_metadata=False,post_metadata_txt_pattern='')
    #L downloads images only
    
    profile = Profile.from_username(L.context, PROFILE)
    
    profileinfo_list.append([profile.username,profile.userid,profile.full_name,profile.followers,profile.followees,profile.biography])
    profileinfo=pd.DataFrame(profileinfo_list)
    profileinfo.columns=['account','account_id','account_fullname','number_of_followers','number_of_followees','biography']
    #'profileinfo' table records each account's information. It can be linked to 'postinfo' table by 'account' or 'account_id'.
    
    
    getpost=profile.get_posts()
    for post in getpost:
        L.download_post(post, PROFILE)
        postinfo_list.append([post.owner_username, post.owner_id, 
                          post.owner_username+"_"+post.date_utc.strftime("%Y-%m-%d_%H-%M-%S")+"_UTC",
                         post.date_utc, post.caption,post.caption_hashtags,post.likes,post.comments,post.is_video])
        
        getcomment=post.get_comments()
        for comm in getcomment:
            comment_list.append([post.owner_username+"_"+post.date_utc.strftime("%Y-%m-%d_%H-%M-%S")+"_UTC",
                                 post.is_video,comm.text,comm.owner,comm.created_at_utc])
    
    postinfo=pd.DataFrame(postinfo_list) 
    postinfo.columns=['account','account_id','post_filename','post_posting_time','post_caption','post_caption_hashtage',
                 'number_of_likes','number_of_comments','if_post_is_a_video']
    #'postinfo' table records each post's information. The 'post' can be image post or video post. Video post can be excluded using 'if_post_is_a_video'.
    #'post_filename' is unique for each post, so it can be the identifier for each post.
        
    comment=pd.DataFrame(comment_list)
    comment.columns=['post_filename','if_post_is_a_video','comment_text','comment_account','comment_time']
    #'comment' table records each post's comments, matching as post1-comment1, post1-comment2, post1-comment3, ..., post2-comment1, post2-comment2, ...
    #The 'post' can be image post or video post. video post can be excluded using 'if_post_is_a_video'.
    #If one post's comment is empty, there will be no comment records for this post.
    #'comment' table can be linked to the 'postinfo' table by the 'post_filename'.
    
    postinfo.to_csv("postinfo.csv")
    comment.to_csv("comment.csv")
    profileinfo.to_csv("profileinfo.csv")
