1. 必须使用简体中文
2. 创建plan的时候，在zzz-doc\zzz-prompt-debug\plan这个文件夹下，文件名和这次需求相关
3. 文档和写的plan都需要在 zzz-doc下面
4. 不需要全局进行es的校验，另外不影响运行的ts错误不需要管，修改ts错误需要向我确认
5. zzz-doc/桌宠前端开发问题修复清单.md，当你修复问题，或者记录问题的时候，记得把问题的原因，解决方案写进去，不断完善这个文档
6. 你产出superspec，或者handoff，或是openspec，创建skills时的文档，反正你产出文档的时候默认使用简体中文，禁止使用英文
7. commit的时候 提交的消息也使用中文
8. 使用context-budget-explore这个skills进行探索和记录
9. 记得使用superspec

### 代码规范

- 可读性优先，使用react-tsx-readability-guard这个skills增强可读性
- 可以参考原来的代码是如何写的

### 组件库

- 默认使用Antd

### 样式

- 样式默认不要使用行内样式，默认使用 css module 使用less或者sass，默认采用外层包裹，内层classname的写法，例如

```css
.wrapper {
  padding: 20px;
  background: #f5f5f5;
  :global {
    .user-info {
      .user-name {
      }
    }
  }
}
```

```tsx
<div className={styles.wrapper}>
  <div className="user-info">
    <span className="user-name">张三</span>
  </div>
</div>
```

- 如果使用 css in js，也是采用外层包裹内层classname的形式，例如

```tsx
export const DetailDiv=styled.div`
  .user-info{
    .user-name{
    }
  }
`
<DetailDiv>
  <div className='user-info'><div/>
  <DetailDiv/>
```
