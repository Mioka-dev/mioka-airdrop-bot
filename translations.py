# translations.py
# All the bot's texts are stored here.

LANGUAGES = ['en', 'jp', 'fr']

TEXTS = {
    'en': {
        'welcome_message': (
            "<b>Welcome to the Mioka Airdrop!</b>\n\n"
            "Mioka is more than just a meme coin — it's a mission. "
            "A samurai-spirited cat fighting in a crypto world filled with economic injustice — "
            "for the people, not the whales. We created Mioka with the genuine aim of helping people, "
            "not just generating profits for the wealthy. Mioka stands for transparency, "
            "honesty, and effective humanitarian support.\n\n"
            "Join our airdrop by completing a few simple tasks to earn **10,000 Mioka Tokens**.\n\n"
            "Here are the tasks:\n"
            "1. Join our Telegram Channel.\n"
            "2. Follow us on Twitter.\n"
            "3. Retweet our pinned post.\n"
            "4. Visit our website.\n\n"
            "You also earn **6,000 tokens** for each direct referral and **4,000 tokens** for each indirect referral. Good luck!"
        ),
        'after_join_telegram_message': "Once you have joined our Telegram channel, click 'Done'.",
        'enter_telegram_username': "Please send your Telegram username (e.g., @MiokaToken):",
        'after_telegram_username_message': "Thank you! Now please follow our Twitter page:",
        'after_follow_twitter_message': "After following, please retweet this post:",
        'after_retweet_message': "When you have retweeted, click 'Done'.",
        'enter_twitter_username': "Please send your Twitter username (e.g., @MiokaToken):",
        'after_twitter_username_message': "Great! Now please visit our website:",
        'after_visit_website_message': "Once you have visited the website, click 'Done'.",
        'enter_wallet_address': "Finally, please send your **BNB Smart Chain (BEP-20)** wallet address to receive your tokens:",
        'thank_you_message': (
            "Thank you for participating in the Mioka Airdrop and for your support!\n\n"
            "Your tokens will be distributed to your wallet after the airdrop ends. "
            "You can earn more tokens by inviting your friends. "
            "Below are your options."
        ),
        'already_joined_message': "You have already participated in the Mioka Airdrop. You can check your status and get your referral link below.",
        'airdrop_finished': "Sorry, the Mioka Airdrop has reached its limit of 4000 participants.",
        'my_tokens_message': "You have earned a total of **{total_tokens}** Mioka Tokens.",
        'your_referral_link_message': "Here is your personal referral link:\n\n{referral_link}\n\nShare it with your friends to earn more tokens!",
        'your_referrals_message': "You have **{direct}** direct referrals and **{indirect}** indirect referrals.",
        'join_telegram_button': "Join Telegram Channel",
        'done_button': "Done",
        'follow_twitter_button': "Follow Twitter",
        'retweet_button': "Retweet this Post",
        'visit_website_button': "Visit Website",
        'my_tokens_button': "My Tokens",
        'my_referral_link_button': "My Referral Link",
        'my_referrals_button': "My Referrals",
    },
    'jp': {
        'welcome_message': (
            "<b>Mioka Airdropへようこそ！</b>\n\n"
            "ミオカは単なるミームコインではありません—それはミッションです。 "
            "経済的不正義に満ちた暗号通貨の世界で戦うサムライ精神を持つ猫— "
            "大口投資家のためではなく、人々のために。私たちは、単に富裕層のために利益を生み出すのではなく、"
            "人々の助けになることを純粋な目的としてミオカを作成しました。ミオカは透明性、"
            "誠実さ、効果的な人道支援を意味します。\n\n"
            "いくつかの簡単なタスクを完了して、<b>10,000 Miokaトークン</b>を獲得しましょう。\n\n"
            "タスクはこちらです：\n"
            "1. Telegramチャンネルに参加する。\n"
            "2. Twitterをフォローする。\n"
            "3. 固定された投稿をリツイートする。\n"
            "4. ウェブサイトを訪問する。\n\n"
            "また、直接の紹介で<b>6,000トークン</b>、間接的な紹介で<b>4,000トークン</b>を獲得できます。頑張ってください！"
        ),
        'after_join_telegram_message': "Telegramチャンネルに参加したら、「完了」をクリックしてください。",
        'enter_telegram_username': "Telegramのユーザー名（例：@MiokaToken）を送信してください：",
        'after_telegram_username_message': "ありがとうございます！次に、Twitterページをフォローしてください：",
        'after_follow_twitter_message': "フォロー後、この投稿をリツイートしてください：",
        'after_retweet_message': "リツイートしたら、「完了」をクリックしてください。",
        'enter_twitter_username': "Twitterのユーザー名（例：@MiokaToken）を送信してください：",
        'after_twitter_username_message': "素晴らしい！次に、ウェブサイトを訪問してください：",
        'after_visit_website_message': "ウェブサイトを訪問したら、「完了」をクリックしてください。",
        'enter_wallet_address': "最後に、トークンを受け取るための<b>BNB Smart Chain (BEP-20)</b>ウォレットアドレスを送信してください：",
        'thank_you_message': (
            "Mioka Airdropへのご参加とご支援ありがとうございます！\n\n"
            "トークンはエアドロップ終了後にウォレットに配布されます。 "
            "友達を招待して、さらに多くのトークンを獲得できます。 "
            "以下にあなたのオプションがあります。"
        ),
        'already_joined_message': "あなたは既にMioka Airdropに参加しています。以下のステータスを確認し、紹介リンクを取得できます。",
        'airdrop_finished': "申し訳ありません、Mioka Airdropは参加者4000人の上限に達しました。",
        'my_tokens_message': "あなたは合計<b>{total_tokens}</b> Miokaトークンを獲得しました。",
        'your_referral_link_message': "あなたの個人紹介リンクはこちらです：\n\n{referral_link}\n\n友達と共有して、さらに多くのトークンを獲得しましょう！",
        'your_referrals_message': "直接の紹介が<b>{direct}</b>人、間接の紹介が<b>{indirect}</b>人です。",
        'join_telegram_button': "Telegramチャンネルに参加",
        'done_button': "完了",
        'follow_twitter_button': "Twitterをフォロー",
        'retweet_button': "この投稿をリツイート",
        'visit_website_button': "ウェブサイトを訪問",
        'my_tokens_button': "私のトークン",
        'my_referral_link_button': "私の紹介リンク",
        'my_referrals_button': "私の紹介者",
    },
    'fr': {
        'welcome_message': (
            "<b>Bienvenue sur Mioka Airdrop !</b>\n\n"
            "Mioka est bien plus qu'un simple meme coin — c'est une mission. "
            "Un chat à l'esprit de samouraï qui se bat dans un monde crypto plein d'injustices économiques — "
            "pour les gens, pas pour les baleines. Nous avons créé Mioka dans le but sincère d'aider les gens, "
            "et non de générer des profits pour les riches. Mioka est synonyme de transparence, "
            "d'honnêteté et de soutien humanitaire efficace.\n\n"
            "Rejoignez notre airdrop en accomplissant quelques tâches simples pour gagner <b>10,000 Tokens Mioka</b>.\n\n"
            "Voici les tâches :\n"
            "1. Rejoignez notre canal Telegram.\n"
            "2. Suivez-nous sur Twitter.\n"
            "3. Retweetez notre publication épinglée.\n"
            "4. Visitez notre site web.\n\n"
            "Vous gagnez également <b>6,000 tokens</b> pour chaque parrainage direct et <b>4,000 tokens</b> pour chaque parrainage indirect. Bonne chance !"
        ),
        'after_join_telegram_message': "Une fois que vous avez rejoint notre canal Telegram, cliquez sur « Fait ».",
        'enter_telegram_username': "Veuillez envoyer votre nom d'utilisateur Telegram (par exemple, @MiokaToken) :",
        'after_telegram_username_message': "Merci ! Maintenant, veuillez suivre notre page Twitter :",
        'after_follow_twitter_message': "Après avoir suivi, veuillez retweeter cette publication :",
        'after_retweet_message': "Lorsque vous avez retweeté, cliquez sur « Fait ».",
        'enter_twitter_username': "Veuillez envoyer votre nom d'utilisateur Twitter (par exemple, @MiokaToken) :",
        'after_twitter_username_message': "Super ! Maintenant, veuillez visiter notre site web :",
        'after_visit_website_message': "Une fois que vous avez visité le site web, cliquez sur « Fait ».",
        'enter_wallet_address': "Enfin, veuillez envoyer votre adresse de portefeuille <b>BNB Smart Chain (BEP-20)</b> pour recevoir vos tokens :",
        'thank_you_message': (
            "Merci d'avoir participé au Mioka Airdrop et pour votre soutien !\n\n"
            "Vos tokens seront distribués à votre portefeuille après la fin de l'airdrop. "
            "Vous pouvez gagner plus de tokens en invitant vos amis. "
            "Ci-dessous, vous trouverez vos options."
        ),
        'already_joined_message': "Vous avez déjà participé au Mioka Airdrop. Vous pouvez vérifier votre statut et obtenir votre lien de parrainage ci-dessous.",
        'airdrop_finished': "Désolé, l'Airdrop Mioka a atteint sa limite de 4000 participants.",
        'my_tokens_message': "Vous avez gagné un total de <b>{total_tokens}</b> Tokens Mioka.",
        'your_referral_link_message': "Voici votre lien de parrainage personnel :\n\n{referral_link}\n\nPartagez-le avec vos amis pour gagner plus de tokens !",
        'your_referrals_message': "Vous avez <b>{direct}</b> parrainages directs et <b>{indirect}</b> parrainages indirects.",
        'join_telegram_button': "Rejoindre le canal Telegram",
        'done_button': "Fait",
        'follow_twitter_button': "Suivre sur Twitter",
        'retweet_button': "Retweeter cette publication",
        'visit_website_button': "Visiter le site web",
        'my_tokens_button': "Mes tokens",
        'my_referral_link_button': "Mon lien de parrainage",
        'my_referrals_button': "Mes parrainages",
    },
}

def get_translation(lang, key):
    return TEXTS.get(lang, TEXTS['en']).get(key, TEXTS['en'][key])