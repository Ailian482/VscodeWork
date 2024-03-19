USE tmc_services;

-- 酒店资源管理二级菜单
insert ignore into admin_staff_resource(id,description,level,menu_no,name,parent_id,resource_type,url,order_number,badge,enable,openable)
values(696313607000035007, NULL, 2, NULL, '酒店资源管理', 1502300000000004, 'menu', 'hotel-resource', 185, NULL, true, true);

-- 酒店资源管理三级菜单
insert ignore into admin_staff_resource(id,description,level,menu_no,name,parent_id,resource_type,url,order_number,badge,enable,openable)
values(696318977663701008, NULL, 3, NULL, '标准酒店信息', 696313607000035007, 'menu', 'standard-hotel', 1, NULL, true, true);
insert ignore into admin_staff_resource(id,description,level,menu_no,name,parent_id,resource_type,url,order_number,badge,enable,openable)
values(696319047226232008, NULL, 3, NULL, '标准数据字典', 696313607000035007, 'menu', 'standard-hotel-dict', 2, NULL, true, true);
insert ignore into admin_staff_resource(id,description,level,menu_no,name,parent_id,resource_type,url,order_number,badge,enable,openable)
values(696319114528034008, NULL, 3, NULL, '标准设施服务', 696313607000035007, 'menu', 'standard-hotel-amenity', 3, NULL, true, true);
insert ignore into admin_staff_resource(id,description,level,menu_no,name,parent_id,resource_type,url,order_number,badge,enable,openable)
values(696319178637971008, NULL, 3, NULL, '供应商匹配管理', 696313607000035007, 'menu', 'supplier-match', 4, NULL, true, true);
insert ignore into admin_staff_resource(id,description,level,menu_no,name,parent_id,resource_type,url,order_number,badge,enable,openable)
values(696319258535268008, NULL, 3, NULL, '供应商酒店列表', 696313607000035007, 'menu', 'supplier-hotel', 5, NULL, true, true);

-- 酒店资源管理四级菜单
insert ignore into admin_staff_resource(id,description,level,menu_no,name,parent_id,resource_type,url,order_number,badge,enable,openable)
values(703194261633503009, NULL, 4, NULL, '供应商数据字典匹配', 696319178637971008, 'menu', 'dict', 1, NULL, true, true);
insert ignore into admin_staff_resource(id,description,level,menu_no,name,parent_id,resource_type,url,order_number,badge,enable,openable)
values(703194419335139009, NULL, 4, NULL, '供应商设施服务匹配', 696319178637971008, 'menu', 'amenity', 2, NULL, true, true);
insert ignore into admin_staff_resource(id,description,level,menu_no,name,parent_id,resource_type,url,order_number,badge,enable,openable)
values(703194482497163009, NULL, 4, NULL, '供应商酒店匹配', 696319178637971008, 'menu', 'hotel', 3, NULL, true, true);

-- 后台功能
insert ignore into admin_function(id,description,enable,level,name,openable,order_number,parent_id)
values ('029927e2-ea31-4902-6708-e276161f6709', NULL, true, '2', '酒店资源管理', true, 18, '1502300000000004');

insert ignore into admin_function(id,description,enable,level,name,openable,order_number,parent_id)
values ('cc52ed3e-17ac-a512-9f5b-44d15q14de75', NULL, true, '3', '标准酒店信息', true, '1', '029927e2-ea31-4902-6708-e276161f6709');
insert ignore into admin_function(id,description,enable,level,name,openable,order_number,parent_id)
values ('cc52ed3e-27ac-a512-9f5b-44d15q24de75', NULL, true, '3', '标准数据字典', true, '2', '029927e2-ea31-4902-6708-e276161f6709');
insert ignore into admin_function(id,description,enable,level,name,openable,order_number,parent_id)
values ('cc52ed3e-37ac-a512-9f5b-44d15q34de75', NULL, true, '3', '标准设施服务', true, '3', '029927e2-ea31-4902-6708-e276161f6709');
insert ignore into admin_function(id,description,enable,level,name,openable,order_number,parent_id)
values ('cc52ed3e-47ac-a512-9f5b-44d15q44de75', NULL, true, '3', '供应商匹配管理', true, '4', '029927e2-ea31-4902-6708-e276161f6709');
insert ignore into admin_function(id,description,enable,level,name,openable,order_number,parent_id)
values ('cc52ed3e-57ac-a512-9f5b-44d15q54de75', NULL, true, '3', '供应商酒店列表', true, '5', '029927e2-ea31-4902-6708-e276161f6709');

insert ignore into admin_function(id,description,enable,level,name,openable,order_number,parent_id)
values ('cc52ed3e-17ac-a541-9f5b-44d15q14de76', NULL, true, '4', '供应商数据字典匹配', true, '1', 'cc52ed3e-47ac-a512-9f5b-44d15q44de75');
insert ignore into admin_function(id,description,enable,level,name,openable,order_number,parent_id)
values ('cc52ed3e-27ac-a542-9f5b-44d15q24de76', NULL, true, '4', '供应商设施服务匹配', true, '2', 'cc52ed3e-47ac-a512-9f5b-44d15q44de75');
insert ignore into admin_function(id,description,enable,level,name,openable,order_number,parent_id)
values ('cc52ed3e-47ac-a543-9f5b-44d15q34de76', NULL, true, '4', '供应商酒店匹配', true, '3', 'cc52ed3e-47ac-a512-9f5b-44d15q44de75');


-- 菜单-功能关联
insert into admin_function_menus(admin_function_id,menus_id) values('029927e2-ea31-4902-6708-e276161f6709','696313607000035007');

insert into admin_function_menus(admin_function_id,menus_id) values('cc52ed3e-17ac-a512-9f5b-44d15q14de75','696318977663701008');
insert into admin_function_menus(admin_function_id,menus_id) values('cc52ed3e-27ac-a512-9f5b-44d15q24de75','696319047226232008');
insert into admin_function_menus(admin_function_id,menus_id) values('cc52ed3e-37ac-a512-9f5b-44d15q34de75','696319114528034008');
insert into admin_function_menus(admin_function_id,menus_id) values('cc52ed3e-47ac-a512-9f5b-44d15q44de75','696319178637971008');
insert into admin_function_menus(admin_function_id,menus_id) values('cc52ed3e-57ac-a512-9f5b-44d15q54de75','696319258535268008');

insert into admin_function_menus(admin_function_id,menus_id) values('cc52ed3e-17ac-a541-9f5b-44d15q14de76','703194261633503009');
insert into admin_function_menus(admin_function_id,menus_id) values('cc52ed3e-27ac-a542-9f5b-44d15q24de76','703194419335139009');
insert into admin_function_menus(admin_function_id,menus_id) values('cc52ed3e-47ac-a543-9f5b-44d15q34de76','703194482497163009');


