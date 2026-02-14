// Persian number conversion
export const toPersianNumber = (num: number | string): string => {
  const persianDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
  return num.toString().replace(/\d/g, (w) => persianDigits[+w]);
};

// Persian date formatting
export const formatPersianDate = (date: string | Date): string => {
  const d = new Date(date);
  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long',
  };
  return new Intl.DateTimeFormat('fa-IR', options).format(d);
};

// Relative time in Persian
export const getRelativeTime = (date: string | Date): string => {
  const now = new Date();
  const d = new Date(date);
  const diffInSeconds = Math.floor((now.getTime() - d.getTime()) / 1000);

  if (diffInSeconds < 60) return 'همین الان';
  if (diffInSeconds < 3600) return `${toPersianNumber(Math.floor(diffInSeconds / 60))} دقیقه پیش`;
  if (diffInSeconds < 86400) return `${toPersianNumber(Math.floor(diffInSeconds / 3600))} ساعت پیش`;
  if (diffInSeconds < 604800) return `${toPersianNumber(Math.floor(diffInSeconds / 86400))} روز پیش`;

  return formatPersianDate(date);
};

// Format currency in Toman
export const formatToman = (amount: number): string => {
  return `${toPersianNumber(amount.toLocaleString())} تومان`;
};

// Persian greeting based on time
export const getPersianGreeting = (): string => {
  const hour = new Date().getHours();
  if (hour < 12) return 'صبح بخیر';
  if (hour < 17) return 'ظهر بخیر';
  if (hour < 21) return 'عصر بخیر';
  return 'شب بخیر';
};