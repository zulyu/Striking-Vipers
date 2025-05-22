#!/bin/bash

# Load configuration
CONFIG_FILE="s3-config.json"
BUCKET_NAME="striking-vipers-game-2024"
REGION="us-east-1"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI is not installed. Please install it first."
    exit 1
fi

# Create S3 bucket if it doesn't exist
if ! aws s3api head-bucket --bucket $BUCKET_NAME 2>/dev/null; then
    echo "Creating S3 bucket: $BUCKET_NAME"
    if [ "$REGION" = "us-east-1" ]; then
        aws s3api create-bucket \
            --bucket $BUCKET_NAME \
            --region $REGION
    else
        aws s3api create-bucket \
            --bucket $BUCKET_NAME \
            --region $REGION \
            --create-bucket-configuration LocationConstraint=$REGION
    fi
fi

# Wait for bucket to be available
echo "Waiting for bucket to be available..."
sleep 5

# Disable block public access settings
echo "Configuring bucket public access settings..."
aws s3api put-public-access-block \
    --bucket $BUCKET_NAME \
    --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"

# Enable static website hosting
echo "Configuring static website hosting..."
aws s3api put-bucket-website \
    --bucket $BUCKET_NAME \
    --website-configuration "{
        \"IndexDocument\": {\"Suffix\": \"index.html\"},
        \"ErrorDocument\": {\"Key\": \"index.html\"}
    }"

# Configure CORS
echo "Configuring CORS..."
aws s3api put-bucket-cors \
    --bucket $BUCKET_NAME \
    --cors-configuration '{
        "CORSRules": [
            {
                "AllowedHeaders": ["*"],
                "AllowedMethods": ["GET"],
                "AllowedOrigins": ["*"],
                "ExposeHeaders": []
            }
        ]
    }'

# Upload files
echo "Uploading files to S3..."
aws s3 sync ../ s3://$BUCKET_NAME/ \
    --exclude "deploy/*" \
    --exclude ".git/*" \
    --exclude "*.pyc" \
    --exclude "__pycache__/*" \
    --exclude "*.db" \
    --exclude "venv/*"

# Set bucket policy for public access
echo "Setting bucket policy..."
aws s3api put-bucket-policy \
    --bucket $BUCKET_NAME \
    --policy "{
        \"Version\": \"2012-10-17\",
        \"Statement\": [
            {
                \"Sid\": \"PublicReadGetObject\",
                \"Effect\": \"Allow\",
                \"Principal\": \"*\",
                \"Action\": \"s3:GetObject\",
                \"Resource\": \"arn:aws:s3:::$BUCKET_NAME/*\"
            }
        ]
    }"

echo "Deployment complete!"
echo "Your game is available at: http://$BUCKET_NAME.s3-website-$REGION.amazonaws.com" 