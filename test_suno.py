import suno

SUNO_COOKIE="__client=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImNsaWVudF8yZ1JiMlFUd0hYTkowZU9BNjNzZTdndENVSHYiLCJyb3RhdGluZ190b2tlbiI6ImZ1OTd1NWY2ZzVpbnFsZGlwZWx3a21rODVyN2V5ZGk5ajQ1a3g2ZTMifQ.odpnNPLX2kv9AipQx-ObkcOlxvR8NUnnFzgMIPazGMx2PLogLdwzOWmx82owflm34clsmUgx6s6z_ePC-g_InaQqtJRnDdVVs3E6bKkWxBUtLTyp-duXCluxPWikMgsKCr63Xno3_f9BgmNHlQGx5oY--eDYuafiRKVG5Kj7lcjIIp95JRm0kUdnMC1TBKsqSQBb9XLu4qz0umHo2yP4SC16-GtLfZ8B0gmGeN-Ekr-8_cAmoiijl7ncpk4ft0t_QWpezLPB8sSiPgMNERMiNut2poogNUGsrWg8dLc3Efu5uN…22%24user_id%22%3A%20%229744c4d5-1a7c-46e2-b2eb-5dba60eb35f2%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22utm_source%22%3A%20%22Klaviyo%22%2C%22utm_medium%22%3A%20%22campaign%22%2C%22utm_campaign%22%3A%20%22Audio%20Input%20Free%22%7D"

client = suno.Suno(cookie='SUNO_COOKIE')

# Generate a song
songs = client.generate(prompt="A serene landscape", is_custom=False, wait_audio=True)

# Download generated songs
for song in songs:
    file_path = client.download(song=song)
    print(f"Song downloaded to: {file_path}")

