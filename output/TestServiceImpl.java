package com.example.service.impl;

import com.example.entity.Test;
import com.example.mapper.TestMapper;
import com.example.service.TestService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import groovy.util.logging.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class TestServiceImpl extends ServiceImpl<TestMapper, Test>
        implements TestService {
}