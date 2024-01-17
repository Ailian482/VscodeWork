use domestic_hotel_resource;

-- 资源平台订单增加预订用户扩展信息
call AddColumnUnlessExists('hotel_order', 'user_ext_info', 'varchar(1000) default null comment "预订用户扩展信息"');

-- 修改部分字段属性
ALTER TABLE supplier_hotel             add  country_name  varchar(30)   null     comment '国家名称';
ALTER TABLE supplier_hotel             add  city_name     varchar(30)   null     comment '城市名称';
ALTER TABLE supplier_hotel             add  district_name varchar(30)   null     comment '行政区名称';
ALTER TABLE supplier_hotel             add  star_name     varchar(30)   null     comment '国家名称';
ALTER TABLE supplier_hotel             add  brand_name    varchar(30)   null     comment '城市名称';
ALTER TABLE supplier_hotel             add  group_name    varchar(30)   null     comment '行政区名称';

-- 添加索引
ALTER TABLE th_hotel ADD INDEX idx_th_hotel_update_time(update_time);
ALTER TABLE supplier_hotel ADD INDEX idx_supplier_hotel_update_time(update_time);