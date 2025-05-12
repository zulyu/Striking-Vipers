# Striking Vipers Web Game

A Python game that teaches data types through matching games.

## Test Account

- Email: test@example.com
- Username: testuser
- Password: password123
- Class Code: CS101

## Building the Game

1. Install the requirements:
```bash
pip install -r requirements.txt
```

2. Build the web version:
```bash
pygbag src/main.py
```

3. Test locally:
The game will be available at http://localhost:8000

## Deploying to AWS S3

1. Create an S3 bucket:
```bash
aws s3 mb s3://your-game-bucket-name
```

2. Configure the bucket for static website hosting:
```bash
aws s3 website s3://your-game-bucket-name --index-document index.html
```

3. Upload the build files:
```bash
aws s3 sync build/web s3://your-game-bucket-name
```

4. Set bucket policy for public access:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::your-game-bucket-name/*"
        }
    ]
}
```

## Using CloudFront (Optional)

1. Create a CloudFront distribution pointing to your S3 bucket
2. Configure the distribution to use the S3 bucket as the origin
3. Set the default root object to index.html
4. Enable HTTPS

## Game Controls

- Click on cards to flip them
- Match data types with their corresponding values
- Use the "Next" button to start a new game
- Use the "Exit" button to close the game

## Development

The game is built using:
- Pygame for game logic
- Pygbag for web deployment
- AWS S3/CloudFront for hosting 