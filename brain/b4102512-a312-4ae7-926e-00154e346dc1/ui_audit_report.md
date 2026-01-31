# 🎨 UI/UX Audit Report - TaiVideo

**Ngày:** 31/01/2026  
**Dự án:** [taivideo](file:///I:/Website/taivideo)  
**Phạm vi:** Giao diện người dùng (Frontend UI/UX)

---

## Summary

| Loại | Số lượng |
|------|----------|
| 🔴 **Critical Issues** | 3 |
| 🟡 **Warnings** | 8 |
| 🟢 **Suggestions** | 6 |

---

## 🔴 Critical Issues (Cần sửa ngay)

### 1. Thiếu `aria-label` cho Icon Buttons

**File:** [Header.tsx](file:///I:/Website/taivideo/src/components/Header.tsx#L143-L148), [Header.tsx](file:///I:/Website/taivideo/src/components/Header.tsx#L181-L186)

**Vấn đề:** Các nút toggle theme và menu hamburger chỉ có icon, không có accessible label.

```tsx
// Line 143-148 - Theme toggle button
<button
  onClick={toggleTheme}
  className={`w-12 h-6 rounded-full...`}
>
  <div className={`w-4 h-4 bg-white rounded-full...`} />
</button>
```

**Nguy hiểm:** Người dùng screen reader (khiếm thị) không biết nút này làm gì.

**Cách sửa:**
```tsx
<button
  onClick={toggleTheme}
  aria-label={theme === 'dark' ? 'Chuyển sang chế độ sáng' : 'Chuyển sang chế độ tối'}
  className={`w-12 h-6 rounded-full...`}
>
```

---

### 2. Input thiếu `autocomplete` và `name` attribute

**File:** [DownloadForm.tsx](file:///I:/Website/taivideo/src/components/DownloadForm.tsx#L25-L31), [InstagramDownload.tsx](file:///I:/Website/taivideo/src/components/InstagramDownload.tsx#L128-L135)

**Vấn đề:** Các input field không có `name` và `autocomplete` attributes.

```tsx
// DownloadForm.tsx line 25-31
<input
  type="text"
  value={link}
  onChange={(e) => setLink(e.target.value)}
  placeholder={t.placeholder}
  className="..."
/>
```

**Nguy hiểm:** 
- Trình duyệt không thể gợi ý auto-fill
- SEO và accessibility kém

**Cách sửa:**
```tsx
<input
  type="url"
  name="video-url"
  autoComplete="url"
  value={link}
  ...
/>
```

---

### 3. Hình ảnh platform icons thiếu kích thước cố định

**File:** [FeatureSection.tsx](file:///I:/Website/taivideo/src/components/FeatureSection.tsx#L96-L100)

**Vấn đề:** Các `<img>` không có `width` và `height` attributes.

```tsx
<img
  src={platform.customIconUrl}
  alt={platform.name}
  className="w-5 h-5 object-contain shrink-0"
/>
```

**Nguy hiểm:** Gây **CLS (Cumulative Layout Shift)** - trang nhảy layout khi ảnh load.

**Cách sửa:**
```tsx
<img
  src={platform.customIconUrl}
  alt={platform.name}
  width={20}
  height={20}
  className="w-5 h-5 object-contain shrink-0"
/>
```

---

## 🟡 Warnings (Nên sửa)

### 4. Thiếu `focus-visible` ring cho các interactive elements

**File:** [DownloadForm.tsx](file:///I:/Website/taivideo/src/components/DownloadForm.tsx#L30), [InstagramDownload.tsx](file:///I:/Website/taivideo/src/components/InstagramDownload.tsx#L134)

**Vấn đề:** Input có `focus:ring-0` hoặc `outline-none` mà không có replacement.

```tsx
// DownloadForm.tsx line 30
className="... focus:ring-0 ..."
```

**Đời thường:** Người dùng navigate bằng keyboard không biết đang focus vào đâu.

**Cách sửa:**
```tsx
className="... focus-visible:ring-2 focus-visible:ring-green-500 ..."
```

---

### 5. Sử dụng `transition: all` ngầm định

**File:** Nhiều components sử dụng `transition-all`

**Vấn đề:** `transition-all` animate MỌI property, gây lag và giật.

**Cách sửa:** Chỉ animate properties cần thiết:
```tsx
// Thay vì
className="transition-all"

// Dùng
className="transition-colors duration-300"
// hoặc
className="transition-transform duration-300"
```

---

### 6. Thiếu `prefers-reduced-motion` support

**File:** [TutorialSection.tsx](file:///I:/Website/taivideo/src/components/TutorialSection.tsx), [FeatureSection.tsx](file:///I:/Website/taivideo/src/components/FeatureSection.tsx)

**Vấn đề:** Animations không tôn trọng user preference cho reduced motion.

**Đời thường:** Người bị say tàu xe hoặc nhạy cảm với chuyển động sẽ khó chịu.

**Cách sửa:** Thêm vào CSS:
```css
@media (prefers-reduced-motion: reduce) {
  .animate-fadeIn,
  .animate-slideUp,
  .animate-bounce,
  .animate-pulse {
    animation: none !important;
    transition: none !important;
  }
}
```

---

### 7. Label không liên kết với input (ContactForm)

**File:** [ContactForm.tsx](file:///I:/Website/taivideo/src/components/ContactForm.tsx#L47-L57)

**Vấn đề:** `<label>` không có `htmlFor` attribute.

```tsx
<label className="block text-base font-semibold...">
  {t.contact.name}
</label>
<input
  type="text"
  ...
/>
```

**Cách sửa:**
```tsx
<label htmlFor="contact-name" className="block text-base font-semibold...">
  {t.contact.name}
</label>
<input
  id="contact-name"
  type="text"
  ...
/>
```

---

### 8. Placeholder không kết thúc bằng `…`

**File:** Tất cả input components

**Vấn đề:** Placeholders kết thúc bằng `...` thay vì ellipsis đúng `…`

```tsx
placeholder="Dán link Instagram (ví dụ: https://www.instagram.com/p/...)"
```

**Cách sửa:**
```tsx
placeholder="Dán link Instagram (ví dụ: https://www.instagram.com/p/…)"
```

---

### 9. Videos thiếu `muted` attribute

**File:** [InstagramDownload.tsx](file:///I:/Website/taivideo/src/components/InstagramDownload.tsx#L187-L192)

**Vấn đề:** Video có thể tự phát âm thanh gây bất ngờ.

```tsx
<video
  src={item.url}
  className="w-full h-full object-cover"
  playsInline
  controlsList="nodownload"
/>
```

**Cách sửa:**
```tsx
<video
  src={item.url}
  muted
  playsInline
  controlsList="nodownload"
  ...
/>
```

---

### 10. Mobile hamburger menu thiếu `aria-expanded`

**File:** [Header.tsx](file:///I:/Website/taivideo/src/components/Header.tsx#L181-L186)

**Vấn đề:** Không thông báo trạng thái menu cho screen reader.

**Cách sửa:**
```tsx
<button
  className="md:hidden p-2..."
  onClick={() => setIsMenuOpen(!isMenuOpen)}
  aria-expanded={isMenuOpen}
  aria-label="Menu điều hướng"
>
```

---

### 11. Logo không có alt text mô tả rõ

**File:** [index.html](file:///I:/Website/taivideo/index.html#L6)

**Vấn đề:** Favicon không ảnh hưởng nhưng logo trong app nên có alt.

---

## 🟢 Suggestions (Tùy chọn - Nâng cao UX)

### 12. Thêm loading skeleton thay vì spinner đơn thuần

**Hiện tại:** Chỉ có Loader2 spinner khi loading.

**Gợi ý:** Thêm skeleton UI cho kết quả download để UX mượt hơn.

---

### 13. Thêm hover states rõ ràng hơn cho cards

**File:** [ResultList.tsx](file:///I:/Website/taivideo/src/components/ResultList.tsx), [FAQSection.tsx](file:///I:/Website/taivideo/src/components/FAQSection.tsx)

**Gợi ý:** Thêm `hover:scale-[1.02]` hoặc `hover:border-green-500` để feedback rõ hơn.

---

### 14. Thêm Dark Mode toggle animation mượt hơn

**Hiện tại:** Toggle chuyển đổi khá đơn giản.

**Gợi ý:** Thêm icon rotation animation khi toggle.

---

### 15. Cải thiện Footer với social links

**File:** [Footer.tsx](file:///I:/Website/taivideo/src/components/Footer.tsx)

**Gợi ý:** Thêm social media icons (Facebook, Zalo, Telegram) để tăng trust.

---

### 16. Thêm "Back to Top" button

**Gợi ý:** Khi scroll xuống, hiện nút floating để quay về đầu trang.

---

### 17. Typography improvements

**Gợi ý:** 
- Sử dụng font từ Google Fonts thay vì system font
- Thêm `text-wrap: balance` cho headings

```css
h1, h2, h3 {
  text-wrap: balance;
}
```

---

## 📋 Next Steps

Anh muốn làm gì tiếp theo?

```
1️⃣ Xem chi tiết từng lỗi với code samples đầy đủ
2️⃣ Sửa lỗi Critical ngay (3 lỗi accessibility)
3️⃣ Sửa tất cả Warnings (8 lỗi)
4️⃣ Áp dụng Suggestions để nâng cao UX
5️⃣ 🔧 FIX ALL - Tự động sửa TẤT CẢ lỗi có thể auto-fix

Gõ số (1-5) để chọn:
```

---

## Checklist tổng hợp

| # | Loại | Vấn đề | File | Auto-fix? |
|---|------|--------|------|-----------|
| 1 | 🔴 | Icon buttons thiếu aria-label | Header.tsx | ✅ |
| 2 | 🔴 | Input thiếu name/autocomplete | DownloadForm, Instagram... | ✅ |
| 3 | 🔴 | Img thiếu width/height | FeatureSection.tsx | ✅ |
| 4 | 🟡 | Thiếu focus-visible | Nhiều files | ✅ |
| 5 | 🟡 | transition-all | Nhiều files | ✅ |
| 6 | 🟡 | prefers-reduced-motion | CSS | ✅ |
| 7 | 🟡 | Label không có htmlFor | ContactForm.tsx | ✅ |
| 8 | 🟡 | Placeholder ... → … | Nhiều files | ✅ |
| 9 | 🟡 | Video thiếu muted | InstagramDownload.tsx | ✅ |
| 10 | 🟡 | aria-expanded | Header.tsx | ✅ |
| 11 | 🟡 | Logo alt text | - | ✅ |
| 12-17 | 🟢 | UX enhancements | Nhiều files | ⚠️ Cần review |
