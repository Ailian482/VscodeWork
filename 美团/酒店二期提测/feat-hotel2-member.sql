use tmc_services;

-- 预订用户扩展信息字段
call AddColumnUnlessExists('hotel_order', 'user_ext_info', 'varchar(1000) default null comment "预订用户扩展信息"');

