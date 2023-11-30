-- User table
CREATE TABLE IF NOT EXISTS map.`user` (
    `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'Primary key',
    `username` varchar(255) NOT NULL COMMENT 'Username',
    `email` varchar(255) NOT NULL COMMENT 'Email',
    `password` varchar(255) NOT NULL COMMENT 'Password',
    `status` tinyint NOT NULL COMMENT 'User status: 0-Regular user, 1-Administrator, 2-Firefighter',
    `create_time` datetime DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT 'Creation time',
    `update_time` datetime DEFAULT CURRENT_TIMESTAMP NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'Update time',
    `is_delete` tinyint DEFAULT 0 NOT NULL COMMENT 'Logical delete'
) COMMENT 'User table';

-- Disaster table
CREATE TABLE IF NOT EXISTS map.`disaster` (
    `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'Primary key',
    `name` varchar(255) NOT NULL COMMENT 'Disaster name',
    `description` text COMMENT 'Disaster description',
    `latitude` varchar(255) COMMENT 'Latitude',
    `longitude` varchar(255) COMMENT 'Longitude',
    `location` varchar(255) COMMENT 'Occurrence location',
    `create_time` datetime DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT 'Creation time',
    `update_time` datetime DEFAULT CURRENT_TIMESTAMP NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'Update time',
    `is_delete` tinyint DEFAULT 0 NOT NULL COMMENT 'Logical delete'
) COMMENT 'Disaster table';

CREATE TABLE IF NOT EXISTS map.`user_disaster_relation`
(
    `id` bigint not null auto_increment comment 'primary key' primary key,
    `userId` bigint not null comment 'user id',
    `disasterId` bigint not null comment 'disaster id',
    `affectedStatus` int default 0 not null comment 'affected status in a disaster, 0-unaffected, 1-affected ',
    `additionalInfo` varchar(255) not null comment 'additional info',
    `createTime` datetime default CURRENT_TIMESTAMP not null comment 'Creation time',
    `updateTime` datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment 'update time',
    `isDelete` tinyint default 0 not null comment 'Logical delete'
) comment '用户与灾难关系';