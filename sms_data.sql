CREATE DATABASE sms;
use sms;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    location TEXT,
    mobileno BIGINT,
    zipcode INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO users (username, email, password) VALUES
('Mohith', 'admin@sms.com', 'password123'),
('user1', 'user1@gmail.com', 'password123'),
('user2', 'user2@gmail.com', 'password123'),
('user3', 'user3@gmail.com', 'password123'),
('user4', 'user4@gmail.com', 'password123');

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    course VARCHAR(100) NOT NULL,
    year INT NOT NULL,
    roll_number VARCHAR(20) NOT NULL UNIQUE,
    city TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO students (first_name, last_name, email, phone, date_of_birth, gender, course, year, roll_number, city
) VALUES

-- First Year Students
('Aarav', 'Sharma', 'aarav.sharma@student.edu.in', '9876543210', '2006-03-15', 'Male', 'Computer Science', 1, '2024CS001', 'Mumbai'),
('Diya', 'Patel', 'diya.patel@student.edu.in', '9876543211', '2006-07-22', 'Female', 'Information Technology', 1, '2024IT001', 'Ahmedabad'),
('Vihaan', 'Kumar', 'vihaan.kumar@student.edu.in', '9876543212', '2006-01-10', 'Male', 'Electronics Engineering', 1, '2024EC001', 'Patna'),
('Ananya', 'Singh', 'ananya.singh@student.edu.in', '9876543213', '2006-05-18', 'Female', 'Computer Science', 1, '2024CS002', 'Lucknow'),
('Arjun', 'Reddy', 'arjun.reddy@student.edu.in', '9876543214', '2006-09-30', 'Male', 'Mechanical Engineering', 1, '2024ME001', 'Hyderabad'),
('Saanvi', 'Nair', 'saanvi.nair@student.edu.in', '9876543215', '2006-11-25', 'Female', 'Civil Engineering', 1, '2024CE001', 'Kochi'),
('Advait', 'Desai', 'advait.desai@student.edu.in', '9876543216', '2006-02-14', 'Male', 'Computer Science', 1, '2024CS003', 'Pune'),
('Myra', 'Chatterjee', 'myra.chatterjee@student.edu.in', '9876543217', '2006-08-08', 'Female', 'Biotechnology', 1, '2024BT001', 'Kolkata'),

-- Second Year Students
('Kabir', 'Mehta', 'kabir.mehta@student.edu.in', '9876543218', '2005-04-20', 'Male', 'Computer Science', 2, '2023CS001', 'Delhi'),
('Aisha', 'Khan', 'aisha.khan@student.edu.in', '9876543219', '2005-06-12', 'Female', 'Information Technology', 2, '2023IT001', 'Jaipur'),
('Reyansh', 'Gupta', 'reyansh.gupta@student.edu.in', '9876543220', '2005-10-05', 'Male', 'Electrical Engineering', 2, '2023EE001', 'Ludhiana'),
('Aadhya', 'Iyer', 'aadhya.iyer@student.edu.in', '9876543221', '2005-12-28', 'Female', 'Computer Science', 2, '2023CS002', 'Bangalore'),
('Vivaan', 'Joshi', 'vivaan.joshi@student.edu.in', '9876543222', '2005-03-17', 'Male', 'Mechanical Engineering', 2, '2023ME001', 'Nagpur'),
('Ishita', 'Pillai', 'ishita.pillai@student.edu.in', '9876543223', '2005-07-09', 'Female', 'Chemical Engineering', 2, '2023CH001', 'Trivandrum'),
('Ayaan', 'Verma', 'ayaan.verma@student.edu.in', '9876543224', '2005-09-14', 'Male', 'Computer Science', 2, '2023CS003', 'Lucknow'),
('Navya', 'Rao', 'navya.rao@student.edu.in', '9876543225', '2005-11-03', 'Female', 'Architecture', 2, '2023AR001', 'Hyderabad'),

-- Third Year Students
('Shaurya', 'Bansal', 'shaurya.bansal@student.edu.in', '9876543226', '2004-02-25', 'Male', 'Computer Science', 3, '2022CS001', 'Delhi'),
('Kiara', 'Kapoor', 'kiara.kapoor@student.edu.in', '9876543227', '2004-05-19', 'Female', 'Information Technology', 3, '2022IT001', 'Mumbai'),
('Dhruv', 'Saxena', 'dhruv.saxena@student.edu.in', '9876543228', '2004-08-11', 'Male', 'Electronics Engineering', 3, '2022EC001', 'Lucknow'),
('Riya', 'Menon', 'riya.menon@student.edu.in', '9876543229', '2004-10-07', 'Female', 'Computer Science', 3, '2022CS002', 'Bangalore'),
('Atharv', 'Pandey', 'atharv.pandey@student.edu.in', '9876543230', '2004-12-15', 'Male', 'Mechanical Engineering', 3, '2022ME001', 'Lucknow'),
('Anvi', 'Ghosh', 'anvi.ghosh@student.edu.in', '9876543231', '2004-01-29', 'Female', 'Civil Engineering', 3, '2022CE001', 'Kolkata'),
('Rudra', 'Malhotra', 'rudra.malhotra@student.edu.in', '9876543232', '2004-04-22', 'Male', 'Computer Science', 3, '2022CS003', 'Delhi'),
('Siya', 'Bhat', 'siya.bhat@student.edu.in', '9876543233', '2004-06-16', 'Female', 'Biotechnology', 3, '2022BT001', 'Bangalore'),

-- Fourth Year Students
('Pranav', 'Agarwal', 'pranav.agarwal@student.edu.in', '9876543234', '2003-03-10', 'Male', 'Computer Science', 4, '2021CS001', 'Delhi'),
('Zara', 'Sheikh', 'zara.sheikh@student.edu.in', '9876543235', '2003-07-05', 'Female', 'Information Technology', 4, '2021IT001', 'Hyderabad'),
('Krishiv', 'Sinha', 'krishiv.sinha@student.edu.in', '9876543236', '2003-09-20', 'Male', 'Electrical Engineering', 4, '2021EE001', 'Patna'),
('Ira', 'Kulkarni', 'ira.kulkarni@student.edu.in', '9876543237', '2003-11-12', 'Female', 'Computer Science', 4, '2021CS002', 'Pune'),
('Aditya', 'Chauhan', 'aditya.chauhan@student.edu.in', '9876543238', '2003-01-08', 'Male', 'Mechanical Engineering', 4, '2021ME001', 'Jaipur'),
('Tara', 'Bhatt', 'tara.bhatt@student.edu.in', '9876543239', '2003-05-24', 'Female', 'Chemical Engineering', 4, '2021CH001', 'Ahmedabad'),
('Veer', 'Thakur', 'veer.thakur@student.edu.in', '9876543240', '2003-08-30', 'Male', 'Computer Science', 4, '2021CS003', 'Shimla'),
('Pari', 'Mohan', 'pari.mohan@student.edu.in', '9876543241', '2003-10-18', 'Female', 'Architecture', 4, '2021AR001', 'Chennai'),

-- Additional Students
('Arnav', 'Jain', 'arnav.jain@student.edu.in', '9876543242', '2005-02-11', 'Male', 'Computer Science', 2, '2023CS004', 'Jaipur'),
('Sana', 'Qureshi', 'sana.qureshi@student.edu.in', '9876543243', '2006-04-27', 'Female', 'Information Technology', 1, '2024IT002', 'Hyderabad'),
('Laksh', 'Chopra', 'laksh.chopra@student.edu.in', '9876543244', '2004-06-09', 'Male', 'Electronics Engineering', 3, '2022EC002', 'Chandigarh'),
('Mahira', 'Das', 'mahira.das@student.edu.in', '9876543245', '2005-08-21', 'Female', 'Computer Science', 2, '2023CS005', 'Bhubaneswar'),
('Yash', 'Rathore', 'yash.rathore@student.edu.in', '9876543246', '2003-12-03', 'Male', 'Mechanical Engineering', 4, '2021ME002', 'Jaipur'),
('Nora', 'Fernandes', 'nora.fernandes@student.edu.in', '9876543247', '2006-09-15', 'Female', 'Civil Engineering', 1, '2024CE002', 'Goa'),
('Hriday', 'Mishra', 'hriday.mishra@student.edu.in', '9876543248', '2004-11-28', 'Male', 'Computer Science', 3, '2022CS004', 'Nagpur'),
('Aanya', 'Tripathi', 'aanya.tripathi@student.edu.in', '9876543249', '2005-01-14', 'Female', 'Biotechnology', 2, '2023BT001', 'Lucknow'),
('Shivansh', 'Bajaj', 'shivansh.bajaj@student.edu.in', '9876543250', '2006-03-06', 'Male', 'Electrical Engineering', 1, '2024EE001', 'Delhi'),
('Mysha', 'Hegde', 'mysha.hegde@student.edu.in', '9876543251', '2003-05-19', 'Female', 'Architecture', 4, '2021AR002', 'Bangalore');

select * from students;
select * from users;
