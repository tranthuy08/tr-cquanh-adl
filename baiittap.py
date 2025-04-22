import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu
movies_data = pd.read_csv("https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/Dataset%20for%20Practice/movies.csv")


# Kiểm tra dữ liệu đầu tiên
st.write("**Preview dữ liệu:**")
st.write(movies_data.head())  # Hiển thị 5 dòng đầu tiên

# Loại bỏ các hàng có giá trị bị thiếu
movies_data = movies_data.dropna()

# Kiểm tra các giá trị trong cột genre(thể loại) và budget(ngân sách)
st.write(movies_data['genre'].unique())  # Kiểm tra các thể loại
st.write(movies_data['budget'].describe())  # Kiểm tra các thống kê của ngân sách #describe: hàm thống kê mô tả

# Lọc theo thể loại
genre_selected = st.selectbox("Chọn thể loại phim:", options=movies_data['genre'].unique()) #selectbox: tạo một hộp chọn
st.write(f"**Danh sách phim thuộc thể loại: {genre_selected}:**")

# Lọc theo năm
year_range = st.slider("Chọn khoảng thời gian phim (năm):", int(movies_data['year'].min()), int(movies_data['year'].max()), 
                       (int(movies_data['year'].min()), int(movies_data['year'].max())))
filtered_data = movies_data[(movies_data['genre'] == genre_selected) & 
                            (movies_data['year'] >= year_range[0]) & 
                            (movies_data['year'] <= year_range[1])]
 # slider: Tạo thanh trượt để chọn khoảng thời gian
# Hiển thị danh sách phim sau khi lọc
st.write(filtered_data[['name', 'genre', 'year', 'budget']])

# Tiêu đề
st.write("""## Average Movie Budget, Grouped by Genre""")

# Tính ngân sách trung bình theo thể loại
avg_budget = movies_data.groupby('genre')['budget'].mean().round()
avg_budget = avg_budget.reset_index()   # reset_index: chuyển đổi avg_budget từ Series thành DataFrame

# Sắp xếp ngân sách trung bình theo thứ tự tăng dần
avg_budget = avg_budget.sort_values(by='budget', ascending=True)
genre = avg_budget['genre']
avg_bud = avg_budget['budget']

# Vẽ biểu đồ cột
fig1 = plt.figure(figsize=(19, 10))
plt.bar(genre, avg_bud, color='maroon')
plt.xlabel('Genre')
plt.ylabel('Average Budget')
plt.title('Matplotlib Bar Chart Showing the Average Budget of Movies in Each Genre')
# Hiển thị biểu đồ cột
st.pyplot(fig1)

# Tiêu đề cho biểu đồ đường
st.write("""## Line Chart Showing Average Budget Sorted by Genre""")
# Vẽ biểu đồ đường
fig2 = plt.figure(figsize=(19, 10))
plt.plot(genre, avg_bud, marker='o', color='blue', linestyle='-', linewidth=2, markersize=8)
plt.xlabel('Genre')
plt.ylabel('Average Budget')
plt.title('Line Chart Showing Average Budget Sorted by Genre')
# Hiển thị biểu đồ đường
st.pyplot(fig2)

# Tiêu đề biểu đồ phân tán 
st.write("## Scatter Plot: Movie Score Distribution by Age Rating")
# Gán mỗi loại rating một giá trị số để vẽ scatter
rating_categories = movies_data['rating'].astype('category') # category: kiểu phân loại
movies_data['rating_code'] = rating_categories.cat.codes # cat.codes: Gán mỗi loại rating 1 mã số nguyên bắt đầu từ 0
# Vẽ biểu đồ scatter 
fig3 = plt.figure(figsize=(12, 8))
plt.scatter(movies_data['rating_code'], movies_data['score'], alpha=0.6, color='purple')
plt.xlabel("Rating (Age Group)")
plt.ylabel("Score")
plt.title("Distribution of Movie Scores by Age Rating")
plt.xticks(movies_data['rating_code'].unique(), rating_categories.cat.categories, rotation=45)
# Hiển thị biểu đồ
st.pyplot(fig3)

# Tính số lượng phim theo quốc gia
country_counts = movies_data['country'].value_counts()
# Lấy top 5 quốc gia 
top_countries = country_counts.head(5)
# Tiêu đề biểu đồ tròn
st.write("## Pie Chart: Movie Distribution by Country (Top 5)")
# Vẽ biểu đồ tròn
fig4 = plt.figure(figsize=(10, 10))
plt.pie(top_countries, labels=top_countries.index, autopct='%1.1f%%', startangle=140)
plt.title("Top 5 Countries with Most Movies")
# Hiển thị biểu đồ
st.pyplot(fig4)
