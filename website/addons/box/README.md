# OSF Box Addon

Enabling the addon for development

1. If `website/addons/box/settings/local.py` does not yet exist, create a local box settings file with `cp website/addons/box/settings/local-dist.py website/addons/box/settings/local.py`
2. Create an app and get a key and secret  (listed as `client_id` and `client_secret`) from <https://app.box.com/developers/services/edit/>.  
3. At the Box app console, add <http://localhost:5000/oauth/callback/box/> to your list of Oauth2 `redirect_uri`.
4. Enter your Box `client_id` and `client_secret` as `BOX_KEY` and `BOX_SECRET` in `website/addons/box/settings/local.py`. 
5. Ensure `"box"` exists in the addons list in `"addons.json"`
