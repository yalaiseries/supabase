# Custom Domain Setup Guide
## Using aihackathon.pro with GitHub Pages

### ✅ Completed Steps

1. **CNAME File Created** - Added to repository root
2. **HTML Files Updated** - Canonical URLs updated to aihackathon.pro
3. **Repository Pushed** - Changes deployed to GitHub

---

## 🔧 Next Steps (Action Required)

### 1. Configure DNS at Your Domain Registrar

Log in to where you purchased `aihackathon.pro` and add these DNS records:

#### A Records (for apex domain aihackathon.pro)
```
Type: A
Name: @ (or blank/root)
Value: 185.199.108.153
TTL: 3600 (or Auto)

Type: A
Name: @
Value: 185.199.109.153
TTL: 3600

Type: A
Name: @
Value: 185.199.110.153
TTL: 3600

Type: A
Name: @
Value: 185.199.111.153
TTL: 3600
```

#### CNAME Record (for www subdomain)
```
Type: CNAME
Name: www
Value: yalaiseries.github.io
TTL: 3600
```

**⏱️ DNS propagation typically takes 1-24 hours**

---

### 2. Configure GitHub Pages

1. Go to: https://github.com/yalaiseries/supabase/settings/pages
2. Under **Custom domain**, enter: `aihackathon.pro`
3. Click **Save**
4. Wait for DNS check (green checkmark appears when verified)
5. ✅ Check **Enforce HTTPS** (do this after DNS is verified)

---

## 📋 URL Structure After Setup

Your website URLs will be:

### Public Pages
- **Home**: https://aihackathon.pro/
- **2026 Collaboration**: https://aihackathon.pro/collaboration.html
- **AI Sharing (Login)**: https://aihackathon.pro/members.html
- **Register**: https://forms.gle/rdZZzCxTVhAAzvCP7 (external)

### Members-Only Pages (after login)
- **Winners Library**: https://aihackathon.pro/winners.html
- **AI/AECO Resources**: https://aihackathon.pro/resources.html

### Fallback URL
- Old GitHub Pages URL will redirect automatically: https://yalaiseries.github.io/supabase/ → https://aihackathon.pro/

---

## ✅ Verification Steps

After DNS propagates and GitHub Pages is configured:

### 1. Test Main Domain
```bash
# Open in browser
https://aihackathon.pro/
```

### 2. Test WWW Redirect
```bash
# Should redirect to aihackathon.pro
https://www.aihackathon.pro/
```

### 3. Test HTTPS
```bash
# Should show secure padlock in browser
https://aihackathon.pro/
```

### 4. Test All Pages
- ✅ https://aihackathon.pro/collaboration.html
- ✅ https://aihackathon.pro/members.html
- ✅ https://aihackathon.pro/winners.html (requires login)
- ✅ https://aihackathon.pro/resources.html (requires login)

---

## 🔍 Troubleshooting

### Issue: DNS Not Resolving
**Check DNS propagation**: https://www.whatsmydns.net/#A/aihackathon.pro

Expected results:
- All A records should show GitHub IPs (185.199.108-111.153)
- CNAME for www should show yalaiseries.github.io

### Issue: "Domain's DNS record could not be retrieved"
**Wait longer** - DNS can take up to 24 hours. Meanwhile:
- Verify DNS records at your registrar
- Use `nslookup aihackathon.pro` or `dig aihackathon.pro` to check

### Issue: HTTPS Not Working
**Don't enable Enforce HTTPS until**:
- ✅ DNS is fully propagated
- ✅ GitHub shows green checkmark next to custom domain
- ⏱️ May take additional time after DNS verification for certificate

### Issue: Old URLs Still Working
**This is normal!** GitHub automatically redirects:
- https://yalaiseries.github.io/supabase/ → https://aihackathon.pro/
- Both URLs will work, but canonical preference is aihackathon.pro

---

## 📝 Common DNS Registrar Instructions

### GoDaddy
1. Go to My Products → Domain Settings
2. Click DNS → Manage Zones
3. Add A and CNAME records as specified above

### Namecheap
1. Domain List → Manage → Advanced DNS
2. Add A Records and CNAME as specified

### Cloudflare
1. DNS → Records → Add record
2. **Important**: Set Proxy status to "DNS only" (gray cloud, not orange)
3. Add A and CNAME records

### Google Domains
1. My Domains → DNS → Custom records
2. Add A and CNAME records as specified

---

## 🎯 Expected Timeline

| Step | Duration | Status |
|------|----------|--------|
| DNS Records Added | Immediate | ⏳ Action Required |
| DNS Propagation | 1-24 hours | ⏳ Waiting |
| GitHub Pages Verification | 5-30 minutes after DNS | ⏳ Pending |
| HTTPS Certificate | 1-2 hours after verification | ⏳ Pending |
| **Site Live** | **24-48 hours max** | 🎉 |

---

## 📞 Support

If issues persist after 48 hours:
1. Check GitHub Pages troubleshooting: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/troubleshooting-custom-domains-and-github-pages
2. Verify DNS with your registrar's support
3. Review GitHub repository settings

---

## ✨ Benefits of Custom Domain

✅ **Professional branding**: aihackathon.pro instead of github.io  
✅ **Better SEO**: Custom domains rank better  
✅ **Easy to remember**: Shorter, cleaner URLs  
✅ **Full HTTPS support**: Automatic SSL certificates  
✅ **Subdomain support**: Can add api.aihackathon.pro, blog.aihackathon.pro later  
✅ **Portability**: Can move hosting later without changing URLs

---

## 🔒 Security Note

After HTTPS is enabled:
- All traffic will be encrypted
- Mixed content warnings resolved
- Supabase authentication works seamlessly
- No code changes needed - everything auto-upgrades to HTTPS

---

Last Updated: January 19, 2026
