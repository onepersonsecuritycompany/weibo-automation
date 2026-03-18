# Weibo Automation API Reference

## Authentication

Weibo uses cookie-based authentication. The two essential cookies are:

### SUBP (Subscription Cookie)
- **Purpose**: Identifies user's subscription status
- **Format**: Base64 encoded string
- **Example**: `0033WrSXqPxfM725Ws9jqgMF55529P9D9WFX3K2sA.7_p_p_p_p_p_p_p`

### SUB (Session Cookie)
- **Purpose**: Maintains user session
- **Format**: Encrypted session token
- **Example**: `_2AkMXyJ...long_string...`

### Obtaining Cookies

1. Log into https://weibo.com in Chrome
2. Open DevTools (F12) → Application → Cookies
3. Find weibo.com domain
4. Copy SUBP and SUB values

## API Endpoints

### Post Tweet

```
POST https://weibo.com/ajax/statuses/update
```

**Headers:**
```
Content-Type: application/x-www-form-urlencoded
X-Requested-With: XMLHttpRequest
Referer: https://weibo.com/
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| content | string | Yes | Tweet text (max 5000 chars) |
| visible | int | No | Visibility: 0=public, 1=friends, 2=private |
| pic_id | string | No | Image ID from upload |

**Response:**
```json
{
  "ok": 1,
  "data": {
    "id": "1234567890123456",
    "mid": "1234567890123456",
    "text": "Tweet content",
    "created_at": "Tue Mar 11 20:30:00 +0800 2025"
  }
}
```

### Upload Image

```
POST https://picupload.weibo.com/interface/pic_upload.php
```

**Headers:**
```
Content-Type: multipart/form-data
Referer: https://weibo.com/
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| pic1 | file | Yes | Image file |
| p | string | Yes | Always "1" |
| upload_source | string | Yes | Always "PC" |

**Response:**
```json
{
  "code": "A00006",
  "data": {
    "pics": {
      "pic_1": {
        "pid": "1234567890123456789012345",
        "size": "large"
      }
    }
  }
}
```

## Error Codes

| Code | Message | Solution |
|------|---------|----------|
| 100001 | 需要登录 | Refresh cookies |
| 100002 | 登录超时 | Re-login and update cookies |
| 100003 | 操作频繁 | Wait and retry |
| 200001 | 内容违规 | Check content guidelines |
| 200002 | 内容重复 | Modify content |
| 200003 | 图片上传失败 | Check image format/size |

## Rate Limits

| Operation | Limit | Window |
|-----------|-------|--------|
| Post tweet | 30 | 1 hour |
| Upload image | 50 | 1 hour |
| Hot search | 60 | 1 minute |

## Content Guidelines

### Allowed Content
- Text up to 5000 characters
- Images: JPG, PNG, GIF (max 20MB)
- Videos: MP4 (max 1GB)
- Up to 18 images per post

### Prohibited Content
- Spam or repetitive content
- Misinformation
- Harassment or abuse
- Copyright violations
- Automated spam patterns

## Best Practices

1. **Cookie Management**
   - Store cookies securely
   - Rotate periodically
   - Monitor for expiration

2. **Error Handling**
   - Implement exponential backoff
   - Check rate limit headers
   - Log errors for debugging

3. **Content Safety**
   - Validate content length
   - Check for prohibited terms
   - Test with non-production account

4. **Performance**
   - Cache timeline data
   - Batch operations when possible
   - Use appropriate timeouts
