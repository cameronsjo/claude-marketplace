# Performance Optimization Skill

Apply performance optimization best practices when analyzing, profiling, or improving application performance.

## When to Use

Invoke this skill when:
- Profiling application performance
- Optimizing slow code or queries
- Analyzing bundle sizes or payload weights
- Designing caching strategies
- Implementing lazy loading
- Investigating performance bottlenecks
- Setting up performance monitoring

## Performance Optimization Approach

### Profile Before Optimizing

**Measure, don't guess**
- Use profiling tools to identify actual bottlenecks
- Establish baseline metrics before optimization
- Focus on the hot path (code that runs most frequently)
- Measure impact of each optimization

**Profiling Tools:**
- **JavaScript/TypeScript:** Chrome DevTools, Lighthouse, Web Vitals
- **Python:** cProfile, py-spy, memory_profiler
- **Database:** EXPLAIN ANALYZE, slow query logs
- **Network:** Browser DevTools Network tab, curl timing

### Watch Bundle Sizes and Payload Weights

**Frontend Optimization:**
- Monitor bundle size with bundler analysis tools
- Tree-shake unused code
- Code split at route/component boundaries
- Analyze third-party dependency weight before adding

**API Optimization:**
- Monitor response payload sizes
- Implement pagination for large datasets
- Use compression (gzip, brotli)
- Return only requested fields (GraphQL, field selection)

**Tools:**
- webpack-bundle-analyzer
- source-map-explorer
- bundlephobia.com (dependency size checking)

### Strategic Caching

**Caching Strategy:**
- Cache at the appropriate level (CDN, server, client, database)
- Use clear invalidation strategies
- Document cache TTLs and reasoning
- Monitor cache hit rates

**Cache Levels:**
1. **CDN/Edge**: Static assets, public content
2. **Application**: Expensive computations, API responses
3. **Database**: Query results, materialized views
4. **Client**: localStorage, IndexedDB, service workers

**Invalidation Strategies:**
- Time-based (TTL)
- Event-based (on data change)
- Version-based (cache busting)
- LRU (Least Recently Used) for memory constraints

### Lazy Loading for Non-Critical Resources

**Lazy Loading Opportunities:**
- Route-based code splitting
- Component-level dynamic imports
- Images below the fold
- Third-party widgets
- Heavy libraries only needed conditionally

**Implementation:**
```javascript
// Route-based splitting
const Dashboard = lazy(() => import('./Dashboard'));

// Component-level
const HeavyChart = lazy(() => import('./HeavyChart'));

// Conditional library loading
if (needsAdvancedFeature) {
  const lib = await import('heavy-library');
}
```

### Monitor Production Performance Metrics

**Key Metrics:**
- **Web Vitals**: LCP, FID/INP, CLS
- **API Performance**: P50, P95, P99 latencies
- **Database**: Query times, connection pool usage
- **Resource Usage**: CPU, memory, network

**Monitoring Tools:**
- Application Performance Monitoring (APM)
- Real User Monitoring (RUM)
- Synthetic monitoring
- OpenTelemetry for distributed tracing

## Performance Patterns

### Database Optimization

**Query Optimization:**
- Use indexes for frequently queried fields
- Avoid N+1 queries (use joins or batch loading)
- Use LIMIT for large result sets
- Consider read replicas for read-heavy workloads

**Connection Pooling:**
- Configure appropriate pool sizes
- Monitor pool saturation
- Use connection timeouts

### Frontend Performance

**React/Vue Optimization:**
- Use React.memo() / computed properties strategically
- Virtualize long lists
- Debounce/throttle expensive operations
- Use Web Workers for heavy computation

**Image Optimization:**
- Use appropriate formats (WebP, AVIF)
- Implement responsive images (srcset)
- Lazy load below-the-fold images
- Use CDN for delivery

### API Performance

**Response Optimization:**
- Implement pagination
- Use field selection/sparse fieldsets
- Enable compression
- Cache responses appropriately

**Request Optimization:**
- Batch similar requests
- Use HTTP/2 multiplexing
- Implement request deduplication
- Use ETags for conditional requests

## Anti-Patterns

**Premature Optimization:**
- ❌ Optimizing before measuring
- ❌ Micro-optimizations that add complexity
- ❌ Optimizing code that rarely runs

**Over-Caching:**
- ❌ Caching without invalidation strategy
- ❌ Caching everything "just in case"
- ❌ Not monitoring cache effectiveness

**Complexity for Marginal Gains:**
- ❌ Adding complexity for <5% improvement
- ❌ Sacrificing readability for minor speedups
- ❌ Optimizing non-bottleneck code

## Performance Checklist

### Before Optimization

- [ ] Established baseline metrics
- [ ] Identified actual bottlenecks through profiling
- [ ] Determined performance goals/SLAs
- [ ] Reviewed monitoring and alerting

### During Optimization

- [ ] Focused on measured bottlenecks
- [ ] Maintained code readability
- [ ] Documented optimization reasoning
- [ ] Added performance tests

### After Optimization

- [ ] Measured improvement against baseline
- [ ] Verified no regressions in other areas
- [ ] Updated documentation
- [ ] Set up ongoing monitoring

## Performance Budget

### Set Budgets

Define performance budgets early:
- Bundle size: < 200KB initial (gzipped)
- Time to Interactive: < 3s on 3G
- API response time: < 200ms P95
- Database queries: < 50ms P95

### Monitor Budgets

- Add CI checks for bundle size
- Alert on budget violations
- Review budgets quarterly
- Adjust based on user impact

## Tools Reference

### Profiling

- **Chrome DevTools**: Performance tab, Lighthouse, Coverage
- **React DevTools**: Profiler tab
- **Python**: cProfile, py-spy, Scalene
- **Node.js**: --inspect, clinic.js

### Monitoring

- **Frontend**: Web Vitals, Lighthouse CI
- **Backend**: OpenTelemetry, Prometheus, Grafana
- **Database**: Query analyzers, slow query logs
- **Network**: HAR files, network timing API

### Analysis

- **Bundle**: webpack-bundle-analyzer, source-map-explorer
- **Dependencies**: bundlephobia, npm-check
- **Images**: ImageOptim, Squoosh
- **Lighthouse**: PageSpeed Insights, web.dev

## Best Practices Summary

1. **Profile first** - Don't optimize without data
2. **Set budgets** - Define acceptable performance thresholds
3. **Cache strategically** - With clear invalidation
4. **Lazy load** - Non-critical resources
5. **Monitor continuously** - Real user metrics
6. **Document reasoning** - Why optimizations were made
7. **Balance trade-offs** - Performance vs complexity vs maintainability

## Resources

- Web Vitals: https://web.dev/vitals/
- Chrome DevTools: https://developer.chrome.com/docs/devtools/
- Python Performance: https://wiki.python.org/moin/PythonSpeed
- Database Indexing: https://use-the-index-luke.com/
