from udio_wrapper import UdioWrapper


auth_token = "_gcl_au=1.1.587904540.1716012611.149980345.1716012823.1716012832; _ga_RF4WWQM7BF=GS1.1.1716015230.2.1.1716015413.38.0.0; _ga=GA1.1.895983895.1716012611; name=value; sb-ssr-production-auth-token.0=%7B%22access_token%22%3A%22eyJhbGciOiJIUzI1NiIsImtpZCI6IlJHVktoVzNNcSsyVzhxcDkiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzE2MDE5MDA4LCJpYXQiOjE3MTYwMTU0MDgsImlzcyI6Imh0dHBzOi8vbWZtcHhqZW1hY3NoZmNwem9zbHUuc3VwYWJhc2UuY28vYXV0aC92MSIsInN1YiI6ImZjYmYwMmIyLTQ0NmItNDY0NS04ZWEwLTU4ZWY0YTQ1MzAxYyIsImVtYW…2C%22updated_at%22%3A%222024-05-18T06%3A56%3A48.132675Z%22%2C%22email%22%3A%22koyasuryu%40gmail.com%22%7D%5D%2C%22created_at%22%3A%222024-04-11T03%3A22%3A15.138528Z%22%2C%22updated_at%22%3A%222024-05-18T06%3A56%3A48.414404Z%22%2C%22is_anonymous%22%3Afalse%7D%2C%22provider_token%22%3A%22ya29.a0AXooCgt4mWNeOxKZcQTRmAIf1rlOcvwedBOTfH0Qt3Rzw93CVruBPYTPw8Tb5_dETTHOyp9LrmWPmC43UgUydaKEvykHM3WfPXYwyiRinRgjEfDX15RLy9BinHszRJXnbnDrRlnMgYJZbJerDwehtgQM4ed9onnZgF58aCgYKASISARESFQHGX2MiGRKb6Yz4dbk1wVEPCh4OvA0171%22%7D"
udio_wrapper = UdioWrapper(auth_token)


short_song_no_download = udio_wrapper.create_song(
    prompt="Relaxing jazz and soulful music",
    seed=-1,
    custom_lyrics="Short song lyrics here"
)
print("Short song generated without downloading:", short_song_no_download)

