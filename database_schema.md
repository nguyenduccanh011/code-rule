# Cấu trúc Database
*Cập nhật lần cuối: 2024-03-24*

## Tổng quan
Database sử dụng PostgreSQL 16 với các bảng chính sau:

## Bảng và Quan hệ

### projects
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | ID duy nhất của project |
| name | VARCHAR(100) | NOT NULL | Tên project |
| description | TEXT | | Mô tả project |
| created_at | TIMESTAMP | NOT NULL DEFAULT now() | Thời điểm tạo |
| updated_at | TIMESTAMP | NOT NULL DEFAULT now() | Thời điểm cập nhật |

### rules
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | ID duy nhất của rule |
| title | VARCHAR(200) | NOT NULL | Tiêu đề rule |
| description | TEXT | NOT NULL | Mô tả chi tiết rule |
| category_id | UUID | FOREIGN KEY | ID của category |
| severity | VARCHAR(20) | NOT NULL | Mức độ nghiêm trọng (low/medium/high) |
| created_at | TIMESTAMP | NOT NULL DEFAULT now() | Thời điểm tạo |
| updated_at | TIMESTAMP | NOT NULL DEFAULT now() | Thời điểm cập nhật |

### categories
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | ID duy nhất của category |
| name | VARCHAR(100) | NOT NULL | Tên category |
| description | TEXT | | Mô tả category |
| created_at | TIMESTAMP | NOT NULL DEFAULT now() | Thời điểm tạo |
| updated_at | TIMESTAMP | NOT NULL DEFAULT now() | Thời điểm cập nhật |

### examples
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | ID duy nhất của example |
| rule_id | UUID | FOREIGN KEY | ID của rule |
| code | TEXT | NOT NULL | Code ví dụ |
| is_good_example | BOOLEAN | NOT NULL | True nếu là ví dụ tốt |
| explanation | TEXT | | Giải thích ví dụ |
| created_at | TIMESTAMP | NOT NULL DEFAULT now() | Thời điểm tạo |
| updated_at | TIMESTAMP | NOT NULL DEFAULT now() | Thời điểm cập nhật |

### project_rules
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| project_id | UUID | FOREIGN KEY | ID của project |
| rule_id | UUID | FOREIGN KEY | ID của rule |
| is_active | BOOLEAN | NOT NULL DEFAULT true | Trạng thái kích hoạt |
| created_at | TIMESTAMP | NOT NULL DEFAULT now() | Thời điểm tạo |
| PRIMARY KEY | (project_id, rule_id) | | Composite key |

### comments
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | ID duy nhất của comment |
| rule_id | UUID | FOREIGN KEY | ID của rule |
| content | TEXT | NOT NULL | Nội dung comment |
| created_at | TIMESTAMP | NOT NULL DEFAULT now() | Thời điểm tạo |
| updated_at | TIMESTAMP | NOT NULL DEFAULT now() | Thời điểm cập nhật |

## Indexes
```sql
-- projects
CREATE INDEX idx_projects_name ON projects(name);

-- rules
CREATE INDEX idx_rules_category ON rules(category_id);
CREATE INDEX idx_rules_title ON rules(title);

-- examples
CREATE INDEX idx_examples_rule ON examples(rule_id);

-- project_rules
CREATE INDEX idx_project_rules_project ON project_rules(project_id);
CREATE INDEX idx_project_rules_rule ON project_rules(rule_id);

-- comments
CREATE INDEX idx_comments_rule ON comments(rule_id);
```

## Constraints
```sql
-- Foreign Keys
ALTER TABLE rules
ADD CONSTRAINT fk_rules_category
FOREIGN KEY (category_id) REFERENCES categories(id);

ALTER TABLE examples
ADD CONSTRAINT fk_examples_rule
FOREIGN KEY (rule_id) REFERENCES rules(id);

ALTER TABLE project_rules
ADD CONSTRAINT fk_project_rules_project
FOREIGN KEY (project_id) REFERENCES projects(id);

ALTER TABLE project_rules
ADD CONSTRAINT fk_project_rules_rule
FOREIGN KEY (rule_id) REFERENCES rules(id);

ALTER TABLE comments
ADD CONSTRAINT fk_comments_rule
FOREIGN KEY (rule_id) REFERENCES rules(id);
``` 