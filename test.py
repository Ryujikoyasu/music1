# from udio_wrapper import UdioWrapper


# # auth_token = "_gcl_au=1.1.587904540.1716012611.149980345.1716012823.1716012832; _ga_RF4WWQM7BF=GS1.1.1716015230.2.1.1716015413.38.0.0; _ga=GA1.1.895983895.1716012611; name=value; sb-ssr-production-auth-token.0=%7B%22access_token%22%3A%22eyJhbGciOiJIUzI1NiIsImtpZCI6IlJHVktoVzNNcSsyVzhxcDkiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzE2MDE5MDA4LCJpYXQiOjE3MTYwMTU0MDgsImlzcyI6Imh0dHBzOi8vbWZtcHhqZW1hY3NoZmNwem9zbHUuc3VwYWJhc2UuY28vYXV0aC92MSIsInN1YiI6ImZjYmYwMmIyLTQ0NmItNDY0NS04ZWEwLTU4ZWY0YTQ1MzAxYyIsImVtYW…2C%22updated_at%22%3A%222024-05-18T06%3A56%3A48.132675Z%22%2C%22email%22%3A%22koyasuryu%40gmail.com%22%7D%5D%2C%22created_at%22%3A%222024-04-11T03%3A22%3A15.138528Z%22%2C%22updated_at%22%3A%222024-05-18T06%3A56%3A48.414404Z%22%2C%22is_anonymous%22%3Afalse%7D%2C%22provider_token%22%3A%22ya29.a0AXooCgt4mWNeOxKZcQTRmAIf1rlOcvwedBOTfH0Qt3Rzw93CVruBPYTPw8Tb5_dETTHOyp9LrmWPmC43UgUydaKEvykHM3WfPXYwyiRinRgjEfDX15RLy9BinHszRJXnbnDrRlnMgYJZbJerDwehtgQM4ed9onnZgF58aCgYKASISARESFQHGX2MiGRKb6Yz4dbk1wVEPCh4OvA0171%22%7D"
# auth_token = "%7B%22access_token%22%3A%22eyJhbGciOiJIUzI1NiIsImtpZCI6IlJHVktoVzNNcSsyVzhxcDkiLCJ0eXAiOiJKV1QifQ.eyJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJvYXV0aCIsInRpbWVzdGFtcCI6MTcxNzAzNzQ0NH1dLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJnb29nbGUiLCJwcm92aWRlcnMiOlsiZ29vZ2xlIl19LCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZW1haWwiOiJrb3lhc3VyeXVAZ21haWwuY29tIiwiZXhwIjoxNzE3MDQxMDQ0LCJpYXQiOjE3MTcwMzc0NDQsImlzX2Fub255bW91cyI6ZmFsc2UsImlzcyI6Imh0dHBzOi8vbWZtcHhqZW1hY3NoZmNwem9zbHUuc3VwYWJhc2UuY28vYXV0aC92MSIsInBob25lIjoiIiwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJzZXNzaW9uX2lkIjoiN2Y4NzBkZTctYWEyZC00ZTU2LTk4NDAtMGNmOGJkMmNkMjA2Iiwic3ViIjoiZmNiZjAyYjItNDQ2Yi00NjQ1LThlYTAtNThlZjRhNDUzMDFjIiwidXNlcl9tZXRhZGF0YSI6eyJhdmF0YXJfdXJsIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTFZyRFp2SXo0WUsyRDV3S2kyNUpYTWdoamdFMEdKcXZGUDFjbFdETVQ2NVgyc0pwZz1zOTYtYyIsImVtYWlsIjoia295YXN1cnl1QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmdWxsX25hbWUiOiJSeXVqaSBLb3lhc3UgKOOCiuOCheOBo-OBmCkiLCJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYW1lIjoiUnl1amkgS295YXN1ICjjgorjgoXjgaPjgZgpIiwicGhvbmVfdmVyaWZpZWQiOmZhbHNlLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EvQUNnOG9jTFZyRFp2SXo0WUsyRDV3S2kyNUpYTWdoamdFMEdKcXZGUDFjbFdETVQ2NVgyc0pwZz1zOTYtYyIsInByb3ZpZGVyX2lkIjoiMTA0MTUyMjMyMDE0MjIzMDkzNTYyIiwic3ViIjoiMTA0MTUyMjMyMDE0MjIzMDkzNTYyIn0sInVzZXJfcm9sZSI6bnVsbH0.Oe83FoEdsKOXT69dhjhG_KDoCNqjh98FCtkGS5_4GUI%22%2C%22token_type%22%3A%22bearer%22%2C%22expires_in%22%3A3600%2C%22expires_at%22%3A1717041044%2C%22refresh_token%22%3A%22V-AXsPtYQxbx0nIS0DVclA%22%2C%22user%22%3A%7B%22id%22%3A%22fcbf02b2-446b-4645-8ea0-58ef4a45301c%22%2C%22aud%22%3A%22authenticated%22%2C%22role%22%3A%22authenticated%22%2C%22email%22%3A%22koyasuryu%40gmail.com%22%2C%22email_confirmed_at%22%3A%222024-04-11T03%3A22%3A15.147663Z%22%2C%22phone%22%3A%22%22%2C%22confirmed_at%22%3A%222024-04-11T03%3A22%3A15.147663Z%22%2C%22last_sign_in_at%22%3A%222024-05-30T02%3A50%3A44.738467026Z%22%2C%22app_metadata%22%3A%7B%22provider%22%3A%22google%22%2C%22providers%22%3A%5B%22google%22%5D%7D%2C%22user_metadata%22%3A%7B%22avatar_url%22%3A%22https%3A%2F%2Flh3.googleusercontent.com%2Fa%2FACg8ocLVrDZvIz4YK2D5wKi25JXMghjgE0GJqvFP1clWDMT65X2sJpg%3Ds96-c%22%2C%22email%22%3A%22koyasuryu%40gmail.com%22%2C%22email_verified%22%3Atrue%2C%22full_name%22%3A%22Ryuji%20Koyasu%20(%E3%82%8A%E3%82%85%E3%81%A3%E3%81%98)%22%2C%22iss%22%3A%22https%3A%2F%2Faccounts.google.com%22%2C%22name%22%3A%22Ryuji%20Koyasu%20(%E3%82%8A%E3%82%85%E3%81%A3%E3%81%98)%22%2C%22phone_verified%22%3Afalse%2C%22picture%22%3A%22https%3A%2F%2Flh3.googleusercontent.com%2Fa%2FACg8ocLVrDZvIz4YK2D5wKi25JXMghjgE0GJqvFP1clWDMT65X2sJpg%3Ds96-c%22%2C%22provider_id%22%3A%22104152232014223093562%22%2C%22sub%22%3A%22104152232014223093562%22%7D%2C%22identities%22%3A%5B%7B%22identity_id%22%3A%22124cc3e1-84fd-4007-a2d2-6a7054e3eace%22%2C%22id%22%3A%22104152232014223093562%22%2C%22user_id%22%3A%22fcbf02b2-446b-4645-8ea0-58ef4a45301c%22%2C%22identity_data%22%3A%7B%22avatar_url%22%3A%22https%3A%2F%2Flh3.googleusercontent.com%2Fa%2FACg8ocLVrDZvIz4YK2D5wKi25JXMghjgE0GJqvFP1clWDMT65X2sJpg%3Ds96-c%22%2C%22email%22%3A%22koyasuryu%40gmail.com%22%2C%22email_verified%22%3Atrue%2C"
# udio_wrapper = UdioWrapper(auth_token)


# short_song_no_download = udio_wrapper.create_song(
#     prompt="Relaxing jazz and soulful music",
#     seed=-1,
#     custom_lyrics="Short song lyrics here"
# )
# print("Short song generated without downloading:", short_song_no_download)


from pydub import AudioSegment

# wavファイルを読み込む
audio = AudioSegment.from_wav("/Users/ryujikoyasu/Downloads/20240629_142012.wav")

# 最初の10秒を抽出する (10秒 = 10,000ミリ秒)
first_10_seconds = audio[:10000]

# 新しいwavファイルとして保存
first_10_seconds.export("output_10_seconds.wav", format="wav")

print("最初の10秒を 'output_10_seconds.wav' に保存しました。")
