// api/profile.ts

export interface ProfileFormData {
  name: string;
  age: number;
  bio: string;
  // добавь нужные поля
}

export async function createProfile(
  profile: ProfileFormData,
  avatar: File,
  token: string
) {
  const formData = new FormData();

  // FastAPI ожидает profile_data как строку JSON
  formData.append("profile_data", JSON.stringify(profile));
  formData.append("avatar", avatar);

  const response = await fetch("/profile/", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`, // если используется JWT
      // ❗ НЕ ДОБАВЛЯЕМ 'Content-Type': 'multipart/form-data'
      // browser сам выставит boundary
    },
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to create profile");
  }

  return response.json();
}
